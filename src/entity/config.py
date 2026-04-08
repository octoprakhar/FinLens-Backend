from dataclasses import dataclass
import os

@dataclass
class IngestConfig:
    md_file_path_dir: str
    md_file_name: str

    chunk_file_path_dir: str
    chunk_file_name: str

    max_word_in_chunk : int = 120


@dataclass
class ProcessingConfig:

    # metadata_dir_path: str
    # metadata_file_name: str

    # faiss_dir_path: str
    # faiss_file_name: str

    chroma_db_path: str

    embedding_model_name: str = "all-MiniLM-L6-v2"

@dataclass
class RagConfig:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY")
    embedding_model_name: str = "all-MiniLM-L6-v2"
