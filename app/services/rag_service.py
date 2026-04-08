import os

from src.entity.artifacts import ProcessingArtifact
from src.entity.config import RagConfig
from src.components.RagPdf import RagPipeline
from app.services.status_service import get_status
from app.services.cache_service import get_cache,set_cache

def ask_pipeline(file_id: str, query: str, debug: bool = False):
    # Check status
    # status = get_status(file_id)
    # if status != 'ready':
    #     return {
    #         "answer": f"Document is {status}. Please wait.",
    #         "sources": []
    #     }
    
    # check cache
    cache_key = (file_id,query)
    cached = get_cache(cache_key)

    if cached:
        return cached
    
    ## Build path
    base_path = os.path.join("data",file_id)
    vector_dir = os.path.join(base_path, "vector_db")

    # metadata_path = os.path.join(vector_dir,"metadata.json")
    # faiss_path = os.path.join(vector_dir,"faiss_index.bin")

    chroma_db_path = os.path.join(base_path,"chroma_db")

    ## LEt's validatE both the paths
    if not os.path.exists(chroma_db_path):
        return {
            "answer": "Invalid file_id or file not processed",
            "sources": []
        }
    
    ## Load RAg
    processing_artifact = ProcessingArtifact(collection_name="finlens_collection", chroma_db_path=chroma_db_path)

    rag_pipeline = RagPipeline(processing_artifact=processing_artifact, config=RagConfig(),file_id=file_id)

    try:
        
        result = rag_pipeline.answer_query(query)

    except Exception as e:
        return {
            "answer": f"Error generating answer: {str(e)}",
            "sources": []
        }
    
    final_result = {
        "answer": result.get("answer", ""),
        "sources": result.get("sources", []) if debug else []
    }
    set_cache(cache_key, final_result)

    return final_result

def retrieve_pipeline(file_id: str, query: str, k: int = 5):

    # Check status
    # status = get_status(file_id)
    # if status != 'ready':
    #     return f"Document is {status}. Please wait."

    base_path = os.path.join("data", file_id)
    # vector_dir = os.path.join(base_path, "vector_db")

    # metadata_path = os.path.join(vector_dir, "metadata.json")
    # faiss_path = os.path.join(vector_dir, "faiss_index.bin")
    chroma_db_path = os.path.join(base_path,"chroma_db")

    if not os.path.exists(chroma_db_path):
        return {"error": "Invalid file_id"}

    processing_artifact = ProcessingArtifact(
        collection_name="finlens_collection",
        chroma_db_path=chroma_db_path
    )

    rag_pipeline = RagPipeline(
        processing_artifact=processing_artifact,
        config=RagConfig(),
        file_id=file_id
    )

    chunks = rag_pipeline.retrieve_chunks(query, k=k)

    return chunks