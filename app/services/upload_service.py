import os

from src.entity.config import IngestConfig, ProcessingConfig
from src.components.ingestor import IngestPdf
from src.components.processPdf import ProcessPdfToVector
from app.services.status_service import set_status

def run_pipeline(file_id: str, file_path: str):
    try:
        base_path = os.path.join("data", file_id)

        processed_dir = os.path.join(base_path, "processed")
        # vector_dir = os.path.join(base_path, "vector_db")
        chroma_db_path = os.path.join(base_path,"chroma_db")

        #------ CONFIGS ---------
        ingest_config = IngestConfig(
            md_file_name="output.md",
            md_file_path_dir=processed_dir,
            chunk_file_path_dir=processed_dir,
            chunk_file_name="chunks.json"
        )

        processing_config = ProcessingConfig(
            # metadata_dir_path=vector_dir,
            # metadata_file_name="metadata.json",
            # faiss_dir_path=vector_dir,
            # faiss_file_name="faiss_index.bin"
            chroma_db_path=chroma_db_path
        )

        #---------- RUN PIPELINE--------
        ingest = IngestPdf(config=ingest_config)
        ingest_artifact = ingest.ingestData(file_source=file_path)

        processor = ProcessPdfToVector(
            ingest_artifact=ingest_artifact,
            config= processing_config
        )

        processor.processPdf()

        # ------ SUCESS -------
        set_status(file_id, "ready")

    except Exception as e:
        set_status(file_id, "failed")
        print(f"[ERROR] {file_id}: {str(e)}")