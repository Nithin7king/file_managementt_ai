from fastembed import TextEmbedding

# Initialize the model using FastEmbed (runs on ONNX Runtime, avoiding heavy PyTorch RAM usage)
# This will download the optimized/quantized version of all-MiniLM-L6-v2 on first run (~45MB).
model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_embedding(text):
    """
    Convert text into a high-precision semantic embedding vector.
    """
    if not text or not text.strip():
        return None

    # FastEmbed expects a list of texts and returns a generator of embeddings
    embeddings = list(model.embed([text.strip()]))
    return embeddings[0]