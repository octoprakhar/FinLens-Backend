from src.entity.config import IngestConfig, ProcessingConfig
from src.components.ingestor import IngestPdf
from src.components.processPdf import ProcessPdfToVector

ingestion_config = IngestConfig(md_file_path_dir="data/processed/",md_file_name="output.md",chunk_file_path_dir="data/processed/", chunk_file_name="chunks.json")
processing_config = ProcessingConfig(metadata_dir_path="data/processed/",metadata_file_name="metadata.json",faiss_dir_path="data/vector_db/",faiss_file_name="faiss_index.bin")

ingestion = IngestPdf(config=ingestion_config)

ingestion_artifact = ingestion.ingestData(file_source="data/uploads/tata-motor.pdf")

processing = ProcessPdfToVector(ingest_artifact=ingestion_artifact,config=processing_config)

processing_artifact = processing.processPdf()

print("Processing completed.")