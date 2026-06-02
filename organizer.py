import os
import shutil
from collections import Counter

def get_cluster_name(cluster_contents):
    """
    Analyzes cluster text to generate a descriptive 2-word folder name.
    """
    if not cluster_contents:
        return "Uncategorized"
    
    # Combine all text and filter for meaningful keywords
    all_text = " ".join(cluster_contents).lower()
    words = all_text.split()
    
    # Filter: Keep words > 4 letters, alphanumeric only, ignore common 'stop words'
    stop_words = {'about', 'their', 'there', 'these', 'would', 'could', 'should', 'extraction', 'content'}
    keywords = [w for w in words if len(w) > 4 and w.isalnum() and w not in stop_words]
    
    # Get the 2 most frequent meaningful words
    most_common = Counter(keywords).most_common(2)
    
    if len(most_common) >= 2:
        return f"{most_common[0][0]}_{most_common[1][0]}".upper()
    elif len(most_common) == 1:
        return f"{most_common[0][0]}".upper()
    
    return "MISCELLANEOUS"

def organize_files(file_paths, labels, root_folder, raw_contents):
    """
    Moves files into AI-named folders and returns the mapping of label IDs to names.
    """
    unique_labels = set(labels)
    cluster_mapping = {}

    # Step 1: Generate Smart Names
    for label in unique_labels:
        if label == -1:
            cluster_mapping[label] = "Uncategorized"
        else:
            # Extract text belonging only to this specific cluster
            cluster_text = [raw_contents[i] for i, l in enumerate(labels) if l == label]
            cluster_mapping[label] = get_cluster_name(cluster_text)

    # Step 2: Physical Organization
    for i, file_path in enumerate(file_paths):
        label = labels[i]
        folder_name = cluster_mapping[label]
        target_path = os.path.join(root_folder, folder_name)
        
        os.makedirs(target_path, exist_ok=True)
        destination = os.path.join(target_path, os.path.basename(file_path))

        # Avoid moving if it's already in the right place
        if os.path.abspath(file_path) != os.path.abspath(destination):
            try:
                shutil.move(file_path, destination)
            except Exception as e:
                print(f"Move error: {e}")
            
    return cluster_mapping