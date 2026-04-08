# from sentence_transformers import SentenceTransformer

# _model = None


# def get_embedding_model(model_name="all-MiniLM-L6-v2"):
#     global _model

#     if _model is None:
#         print("🔄 Loading embedding model...")
#         _model = SentenceTransformer(model_name)

#     return _model

from langchain_huggingface import HuggingFaceEmbeddings
_model = None

def get_embedding_model(model_name="all-MiniLM-L6-v2"):
    global _model

    if _model is None:
        print("🔄 Loading embedding model...")
        _model = HuggingFaceEmbeddings(model_name=model_name)

    return _model