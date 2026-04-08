from sentence_transformers import SentenceTransformer

# Load once (important)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    return model.encode(text)
