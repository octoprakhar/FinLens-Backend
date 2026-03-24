from src.entity.config import IngestConfig
from src.components.ingestor import IngestPdf

ingestion_config = IngestConfig(md_file_path_dir="data/processed/",md_file_name="output.md",chunk_file_path_dir="data/processed/", chunk_file_name="chunks.json")

ingestion = IngestPdf(config=ingestion_config)

ingestion_artifact = ingestion.ingestData(file_source="data/uploads/tata-motor.pdf")

print("Ingestion Completed.")