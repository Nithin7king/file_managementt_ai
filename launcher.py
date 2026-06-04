"""
SEFS Launcher — Auto-opens browser when running as a packaged .exe
This replaces the __main__ block for the PyInstaller build.
"""
import os
import sys
import time
import threading
import webbrowser
import platform

# Make sure we run from the directory the exe is in
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

# Suppress TF warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

PORT = 5000

def open_browser():
    time.sleep(3)  # Wait for Flask to start
    webbrowser.open(f"http://127.0.0.1:{PORT}")

if __name__ == "__main__":
    ROOT_FOLDER = "root_folder"
    if not os.path.exists(ROOT_FOLDER):
        os.makedirs(ROOT_FOLDER)

    print("\n" + "="*50)
    print("   SEFS NEURAL INTERFACE — LOCAL MODE")
    print(f"   Starting at http://127.0.0.1:{PORT}")
    print("   Your browser will open automatically...")
    print("   Drop files into the 'root_folder' directory")
    print("="*50 + "\n")

    # Import SEFS modules
    from main import app, process_all_files, ROOT_FOLDER as RF

    # Start file watcher (Windows only)
    if platform.system() == "Windows":
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class SEFSHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                if not event.is_directory and not event.src_path.endswith(".json"):
                    threading.Timer(2, process_all_files).start()

        observer = Observer()
        observer.schedule(SEFSHandler(), RF, recursive=True)
        observer.start()

    # Initial scan
    process_all_files()

    # Open browser in background
    threading.Thread(target=open_browser, daemon=True).start()

    # Run Flask (blocking)
    app.run(host='127.0.0.1', port=PORT, debug=False, use_reloader=False)
