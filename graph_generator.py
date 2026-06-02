import os
import json
import time
from file_reader import get_summary

def load_security_registry():
    """
    Reads the dynamic security database to check for locked files.
    """
    if os.path.exists("security_registry.json"):
        try:
            with open("security_registry.json", "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def generate_graph(file_paths, embeddings, labels, raw_contents, cluster_mapping):
    """
    Translates SEFS intelligence into a secure Neural Map.
    Now supports Dynamic Right-Click Security and AI-generated Smart Names.
    """
    nodes = []
    edges = []

    # System Core Node (The root of the neural brain)
    nodes.append({
        "data": {"id": "root", "label": "ROOT_SYSTEM", "type": "root", "color": "#FF5733"}
    })

    # Step 1: Create Folder Nodes using AI-generated Smart Names
    for label_id, folder_name in cluster_mapping.items():
        nodes.append({
            "data": {
                "id": folder_name, 
                "label": folder_name, 
                "type": "folder", 
                "color": "#33C1FF"
            }
        })
        edges.append({"data": {"source": "root", "target": folder_name}})

    # Load the dynamic registry for security status
    security_db = load_security_registry()

    # Step 2: Create Secure File Nodes
    for i, file_path in enumerate(file_paths):
        file_name = os.path.basename(file_path)
        label_id = labels[i]
        folder_name = cluster_mapping[label_id]

        # Construct the path for metadata retrieval
        new_actual_path = os.path.join("root_folder", folder_name, file_name)
        
        # DYNAMIC SECURITY CHECK:
        # Check if this specific filename exists in our security registry
        is_locked = file_name in security_db
        stored_password = security_db.get(file_name, "")
        
        # Metadata Extraction
        created_time = "N/A"
        if os.path.exists(new_actual_path):
            created_time = time.ctime(os.path.getctime(new_actual_path))

        # Formatting for UI
        ext = os.path.splitext(file_name)[1].lower().replace('.', '').upper()
        
        # AI Summarization
        raw_sum = get_summary(raw_contents[i])
        clean_summary = raw_sum.replace("\n", " ").strip()
        if len(clean_summary) > 400:
            clean_summary = clean_summary[:397] + "..."

        nodes.append({
            "data": {
                "id": file_name,
                "label": f"{'🔒 ' if is_locked else ''}[{ext}] {file_name}",
                "type": "file",
                # Visual Feedback: RED (#FF3333) for locked, GREEN (#75FF33) for open
                "color": "#FF3333" if is_locked else "#75FF33",
                "locked": is_locked,
                "password": stored_password, # Uses the dynamic password from registry
                "summary": clean_summary,
                "created": created_time,
                "path": os.path.abspath(new_actual_path)
            }
        })
        edges.append({"data": {"source": folder_name, "target": file_name}})

    # Final Output to JSON for Cytoscape
    with open("graph_data.json", "w") as f:
        json.dump({"nodes": nodes, "edges": edges}, f)