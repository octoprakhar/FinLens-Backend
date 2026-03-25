import faiss
import json

INDEX_CACHE = {}
METADATA_CACHE = {}

def get_vector_store(file_id: str, faiss_path: str, metadata_path: str):
    
    # Cache Hit
    if file_id in INDEX_CACHE and file_id in METADATA_CACHE:
        return INDEX_CACHE[file_id], METADATA_CACHE[file_id]
    
    print(f"Loading FAISS + metadata for {file_id}")

    # Load from disk
    index = faiss.read_index(faiss_path)

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    
    # Store in Cache
    INDEX_CACHE[file_id] = index
    METADATA_CACHE[file_id] = metadata

    return index, metadata

def clear_vector_store(file_id: str):
    if file_id in INDEX_CACHE:
        del INDEX_CACHE[file_id]

    if file_id in METADATA_CACHE:
        del METADATA_CACHE[file_id]
