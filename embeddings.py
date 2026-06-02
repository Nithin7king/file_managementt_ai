from sentence_transformers import SentenceTransformer

# Upgrading to all-mpnet-base-v2 for maximum semantic accuracy
# Note: This will download a ~420MB model on first run.
model = SentenceTransformer('all-mpnet-base-v2')

def get_embedding(text):
    """
    Convert text into a high-precision semantic embedding vector.
    """
    if not text or not text.strip():
        return None

    # Normalizing text slightly helps embedding quality
    embedding = model.encode(text.strip())
    return embedding