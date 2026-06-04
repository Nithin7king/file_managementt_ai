from sentence_transformers import SentenceTransformer

# Upgrading to all-MiniLM-L6-v2 to fit within Render's 512MB Free Tier limits
# Note: This will download a ~80MB model on first run.
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """
    Convert text into a high-precision semantic embedding vector.
    """
    if not text or not text.strip():
        return None

    # Normalizing text slightly helps embedding quality
    embedding = model.encode(text.strip())
    return embedding