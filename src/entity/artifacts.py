from dataclasses import dataclass

@dataclass
class IngestArtifact:
    md_file_path: str
    chunk_file_path: str

@dataclass
class ProcessingArtifact:
    metadata_file_path: str
    faiss_file_path: str