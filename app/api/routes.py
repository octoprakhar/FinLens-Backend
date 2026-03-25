from fastapi import APIRouter, UploadFile, File
import uuid
import os
import shutil

from src.entity.config import IngestConfig,ProcessingConfig,RagConfig
from src.entity.artifacts import ProcessingArtifact
from src.components.ingestor import IngestPdf
from src.components.processPdf import ProcessPdfToVector
from src.components.RagPdf import RagPipeline

from app.schemas.response import UploadPdfResponse, QueryResponse
from app.schemas.request import QueryRequest

router = APIRouter()
CACHE = {}

@router.get("/health")
def health():
    return {"status":"ok"}



@router.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    try:
        # Create file id
        file_id = str(uuid.uuid4())

        ## Let's create folder structure
        base_path = os.path.join("data",file_id)

        upload_dir = os.path.join(base_path,"uploads")
        processed_dir = os.path.join(base_path,"processed")
        vector_dir = os.path.join(base_path, "vector_db")

        os.makedirs(upload_dir,exist_ok=True)
        os.makedirs(processed_dir,exist_ok=True)
        os.makedirs(vector_dir,exist_ok=True)

        ## Save file
        file_path = os.path.join(upload_dir,file.filename)

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        ## Configs
        ingest_config = IngestConfig(
            md_file_path_dir=processed_dir,
            md_file_name="output.md",
            chunk_file_path_dir=processed_dir,
            chunk_file_name="chunks.json"
        )

        processing_config = ProcessingConfig(
            metadata_dir_path=vector_dir,
            metadata_file_name="metadata.json",
            faiss_dir_path=vector_dir,
            faiss_file_name="faiss_index.bin"
        )

        ## Runing the pipeline
        ingest = IngestPdf(config=ingest_config)
        ingest_artifact = ingest.ingestData(file_source=file_path)

        processor = ProcessPdfToVector(ingest_artifact=ingest_artifact,config=processing_config)
        processor.processPdf()

        ## Sending the response
        return UploadPdfResponse(status=200,file_id=file_id)
    
    except Exception as e:
        return UploadPdfResponse(status=500,file_id="",error=str(e))
    

@router.post("/ask", response_model = QueryResponse)
def ask_question(request: QueryRequest):
    file_id = request.file_id
    query = request.query

    cache_key = (file_id,query)

    if cache_key in CACHE:
        return QueryResponse(answer=CACHE[cache_key])

    ## Building the paths
    base_path = os.path.join("data", file_id)
    vector_dir = os.path.join(base_path,"vector_db")

    metadata_path = os.path.join(vector_dir,"metadata.json")
    faiss_path = os.path.join(vector_dir,"faiss_index.bin")

    ## Validation
    if not os.path.exists(metadata_path) or not os.path.exists(faiss_path):
        return {
            "answer": "Invalid file_id or file not processed"
        }
    
    ## LOading artifacts
    processing_artifact = ProcessingArtifact(metadata_file_path=metadata_path, faiss_file_path=faiss_path)

    ## Init RAG
    rag_config = RagConfig()
    rag_pipeline = RagPipeline(processing_artifact=processing_artifact,config=rag_config)

    answer = rag_pipeline.answer_query(query)

    CACHE[cache_key] = answer

    return QueryResponse(answer=answer)

@router.post("/retrieve")
def retrieve_chunks(request: QueryRequest):
    file_id = request.file_id
    query = request.query

    base_path = os.path.join("data",file_id)
    vector_dir = os.path.join(base_path, "vector_db")

    metadata_path = os.path.join(vector_dir,"metadata.json")
    faiss_path = os.path.join(vector_dir,"faiss_index.bin")

    if not os.path.exists(metadata_path):
        return {"error":"Invalid file_id"}
    
    processing_artifact = ProcessingArtifact(
        metadata_file_path=metadata_path,
        faiss_file_path=faiss_path
    )

    rag = RagPipeline(processing_artifact=processing_artifact,config=RagConfig())

    chunks = rag.retrieve_chunks(query=query)

    return {
        "chunks": chunks
    }

@router.delete("/cleanup/{file_id}")
def cleanup(file_id: str):
    base_path = os.path.join("data", file_id)
    
    if not os.path.exists(base_path):
        return {"message":"File not found"}
    
    shutil.rmtree(base_path)

    # Also remove cache entries
    keys_to_delete = [k for k in CACHE if k[0] == file_id]
    for k in keys_to_delete:
        del CACHE[k]

    return {"message": "Deleted successfully"}