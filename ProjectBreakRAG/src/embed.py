from langchain_huggingface import HuggingFaceEmbeddings

def obtener_embeddings():
    """
    Devuelve el modelo de embeddings local.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )