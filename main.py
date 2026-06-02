import os
import time
import threading
import subprocess
import json
from flask import Flask, render_template, jsonify, send_from_directory, request
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tqdm import tqdm

# Suppress technical warnings for a cleaner demo console
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

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
            if file.lower().endswith((".pdf", ".txt", ".docx", ".pptx", ".png", ".jpg", ".jpeg")):
                all_files.append(os.path.join(root, file))

    if not all_files:
        print("[SEFS] System Idle: No compatible files found.\n")
        return

    # Progress bar for terminal visualization
    for full_path in tqdm(all_files, desc="Neural Scan", unit="file", colour="green"):
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
            # Smart Folder Naming and Physical Organization
            cluster_mapping = organize_files(file_paths, labels, ROOT_FOLDER, raw_contents)
            
            # Generate the JSON map for the UI
            generate_graph(file_paths, embeddings, labels, raw_contents, cluster_mapping)
            print(f"\n[SEFS] Intelligence Sync Complete. Clusters: {len(cluster_mapping)}\n")
    else:
        print("\n[SEFS] System Idle: Insufficient data nodes.\n")

def debounce_process():
    global debounce_timer
    if debounce_timer:
        debounce_timer.cancel()
    debounce_timer = threading.Timer(DEBOUNCE_DELAY, process_all_files)
    debounce_timer.start()

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

@app.route('/lock-node', methods=['POST'])
def lock_node():
    """Triggered by right-click 'Make Private' in UI."""
    data = request.json
    filename = data.get('filename')
    password = data.get('password')
    
    db = get_security_data()
    db[filename] = password
    save_security_data(db)
    
    # FORCE SYNC: Re-generate the graph so the node turns Red immediately
    process_all_files()
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
        # FORCE SYNC: Re-generate the graph so the node turns Green immediately
        process_all_files()
        return jsonify({"status": "unlocked"})
    return jsonify({"status": "wrong_password"}), 403

@app.route('/open-folder/<path:filename>')
def open_folder(filename):
    """Verifies security registry before opening file in OS."""
    try:
        user_password = request.args.get('password')
        db = get_security_data()
        
        # Registry-based security check
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

def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    if not os.path.exists(ROOT_FOLDER):
        os.makedirs(ROOT_FOLDER)

    observer = Observer()
    observer.schedule(SEFSHandler(), ROOT_FOLDER, recursive=True)
    observer.start()

    process_all_files()

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    print("\n" + "="*40)
    print(">>> SEFS DYNAMIC SECURITY ONLINE <<<")
    print("INTERFACE: http://127.0.0.1:5000")
    print("="*40 + "\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()