# clustering.py

import numpy as np
import hdbscan

def cluster_embeddings(embeddings):
    """
    Cluster file embeddings using HDBSCAN.
    Returns cluster labels.
    """

    if len(embeddings) < 2:
        return None

    clusterer = hdbscan.HDBSCAN(min_cluster_size=2)
    labels = clusterer.fit_predict(np.array(embeddings))

    return labels
