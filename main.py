import os
import time
import threading
import json
import platform
from flask import Flask, render_template, jsonify, send_from_directory, request, send_file

# Suppress technical warnings for a cleaner demo console
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Detect if running in cloud environment (no display / not Windows)
IS_CLOUD = not (platform.system() == "Windows")

# Import watchdog only when running locally
if not IS_CLOUD:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

# Import your custom SEFS modules
from file_reader import read_file
from embeddings import get_embedding
from clustering import cluster_embeddings
from organizer import organize_files
from graph_generator import generate_graph

# Configuration
app = Flask(__name__, template_folder='frontend', static_folder='.')
ROOT_FOLDER = "root_folder"
SECURITY_DB = "security_registry.json"
DEBOUNCE_DELAY = 2  # Seconds to wait for file drops to finish
debounce_timer = None
ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.docx', '.pptx', '.png', '.jpg', '.jpeg'}

# --- DYNAMIC SECURITY DATABASE HELPERS ---

def get_security_data():
    """Reads the current lock status of all files from the registry."""
    if os.path.exists(SECURITY_DB):
        try:
            with open(SECURITY_DB, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_security_data(data):
    """Saves the privacy registry to a persistent JSON file."""
    with open(SECURITY_DB, "w") as f:
        json.dump(data, f, indent=4)

# --- CORE NEURAL ENGINE ---

def process_all_files():
    """
    The SEFS Neural Engine:
    1. Scans files and extracts text.
    2. Clusters data semantically.
    3. Triggers graph generation with security awareness.
    """
    print("\n[SEFS] Neural Engine: Initiating deep semantic analysis...")
    file_paths, embeddings, raw_contents = [], [], []

    all_files = []
    for root, dirs, files in os.walk(ROOT_FOLDER):
        for file in files:
            if os.path.splitext(file)[1].lower() in ALLOWED_EXTENSIONS:
                all_files.append(os.path.join(root, file))

    if not all_files:
        print("[SEFS] System Idle: No compatible files found.\n")
        return

    for full_path in all_files:
        content = read_file(full_path)
        if content and len(content.strip()) > 10:
            embedding = get_embedding(content)
            if embedding is not None:
                file_paths.append(full_path)
                embeddings.append(embedding)
                raw_contents.append(content)

    if len(embeddings) >= 2:
        labels = cluster_embeddings(embeddings)
        if labels is not None:
            cluster_mapping = organize_files(file_paths, labels, ROOT_FOLDER, raw_contents)
            generate_graph(file_paths, embeddings, labels, raw_contents, cluster_mapping)
            print(f"\n[SEFS] Intelligence Sync Complete. Clusters: {len(cluster_mapping)}\n")
    elif len(embeddings) == 1:
        # Handle single file gracefully
        file_paths_list = [file_paths[0]]
        cluster_mapping = {0: "SINGLE_FILE"}
        generate_graph(file_paths_list, embeddings, [0], raw_contents, cluster_mapping)
    else:
        print("\n[SEFS] System Idle: Insufficient data nodes.\n")

def debounce_process():
    global debounce_timer
    if debounce_timer:
        debounce_timer.cancel()
    debounce_timer = threading.Timer(DEBOUNCE_DELAY, process_all_files)
    debounce_timer.start()

if not IS_CLOUD:
    class SEFSHandler(FileSystemEventHandler):
        def on_any_event(self, event):
            if not event.is_directory and not event.src_path.endswith(".json"):
                debounce_process()

# --- NEURAL INTERFACE ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph_data.json')
def get_graph_data():
    return send_from_directory('.', 'graph_data.json')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Cloud-compatible drag-and-drop file upload endpoint."""
    uploaded = request.files.getlist('files')
    if not uploaded:
        return jsonify({"status": "error", "message": "No files received"}), 400

    os.makedirs(ROOT_FOLDER, exist_ok=True)
    saved = []
    for file in uploaded:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext in ALLOWED_EXTENSIONS:
            dest = os.path.join(ROOT_FOLDER, file.filename)
            file.save(dest)
            saved.append(file.filename)

    if not saved:
        return jsonify({"status": "error", "message": "No valid file types uploaded"}), 400

    # Run processing in background thread
    threading.Thread(target=process_all_files, daemon=True).start()
    return jsonify({"status": "processing", "files": saved})

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download a file from root_folder (cloud replacement for open-in-explorer)."""
    try:
        user_password = request.args.get('password', '')
        db = get_security_data()

        if filename in db and db[filename] != user_password:
            return jsonify({"status": "denied", "message": "Neural Handshake Failed"}), 403

        full_root = os.path.abspath(ROOT_FOLDER)
        for root, dirs, files in os.walk(full_root):
            if filename in files:
                target_path = os.path.join(root, filename)
                return send_file(target_path, as_attachment=True)

        return jsonify({"status": "file not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/open-folder/<path:filename>')
def open_folder(filename):
    """
    LOCAL: Opens file in Windows Explorer.
    CLOUD: Falls back to download.
    """
    if IS_CLOUD:
        # Redirect to download on cloud
        password = request.args.get('password', '')
        return download_file(filename) if not password else download_file(filename)

    try:
        import subprocess
        user_password = request.args.get('password')
        db = get_security_data()

        if filename in db and db[filename] != user_password:
            return jsonify({"status": "denied", "message": "Neural Handshake Failed"}), 403

        full_root = os.path.abspath(ROOT_FOLDER)
        for root, dirs, files in os.walk(full_root):
            if filename in files:
                target_path = os.path.join(root, filename)
                normalized_path = os.path.normpath(target_path)
                subprocess.Popen(f'explorer /select,"{normalized_path}"')
                return jsonify({"status": "success"})
        return jsonify({"status": "file not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/lock-node', methods=['POST'])
def lock_node():
    """Triggered by right-click 'Make Private' in UI."""
    data = request.json
    filename = data.get('filename')
    password = data.get('password')

    db = get_security_data()
    db[filename] = password
    save_security_data(db)

    threading.Thread(target=process_all_files, daemon=True).start()
    return jsonify({"status": "locked"})

@app.route('/unlock-node', methods=['POST'])
def unlock_node():
    """Triggered by right-click 'Remove Privacy' in UI."""
    data = request.json
    filename = data.get('filename')
    password = data.get('password')

    db = get_security_data()
    if db.get(filename) == password:
        del db[filename]
        save_security_data(db)
        threading.Thread(target=process_all_files, daemon=True).start()
        return jsonify({"status": "unlocked"})
    return jsonify({"status": "wrong_password"}), 403

@app.route('/status')
def status():
    """Health check endpoint."""
    return jsonify({"status": "online", "mode": "cloud" if IS_CLOUD else "local"})

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    if not os.path.exists(ROOT_FOLDER):
        os.makedirs(ROOT_FOLDER)

    if not IS_CLOUD:
        observer = Observer()
        observer.schedule(SEFSHandler(), ROOT_FOLDER, recursive=True)
        observer.start()

    process_all_files()

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    print("\n" + "="*40)
    print(">>> SEFS DYNAMIC SECURITY ONLINE <<<")
    print(f"INTERFACE: http://127.0.0.1:5000")
    print(f"MODE: {'CLOUD' if IS_CLOUD else 'LOCAL'}")
    print("="*40 + "\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        if not IS_CLOUD:
            observer.stop()
    if not IS_CLOUD:
        observer.join()