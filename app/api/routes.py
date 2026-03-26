from fastapi import APIRouter, UploadFile, File, BackgroundTasks
import uuid
import os
import shutil

from app.schemas.response import UploadPdfResponse, QueryResponse
from app.schemas.request import QueryRequest
from app.services.upload_service import run_pipeline
from app.services.status_service import set_status, get_status
from app.services.rag_service import retrieve_pipeline,ask_pipeline
from app.services.cache_service import clear_cache_by_file


router = APIRouter()

@router.get("/health")
def health():
    return {"status":"ok"}



@router.post("/upload")
def upload_pdf(file: UploadFile = File(...), bg: BackgroundTasks = None):

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
        file_path = os.path.join(upload_dir,"input.pdf")

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        set_status(file_id=file_id,status= "processing")

        ## Run background task
        bg.add_task(run_pipeline, file_id, file_path)

        ## ------- RESPONSE -------------
        return UploadPdfResponse(
            status=200,
            file_id = file_id,
            message="Processing started"
        )
    
    except Exception as e:
        return UploadPdfResponse(
            status=500,
            file_id="",
            error=str(e)
        )
    

@router.get("/status/{file_id}")
def check_status(file_id: str):
    status = get_status(file_id)

    return {
        "file_id": file_id,
        "status":status
    }
        


@router.post("/ask", response_model = QueryResponse)
def ask_question(request: QueryRequest):
    result = ask_pipeline(file_id=request.file_id, query=request.query, debug=request.debug)

    return QueryResponse(
    answer=result["answer"],
    sources=result["sources"] or None
)

@router.post("/retrieve")
def retrieve_chunks(request: QueryRequest):
    file_id = request.file_id
    query = request.query

    chunks = retrieve_pipeline(
        file_id=file_id,query=query
    )


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
    clear_cache_by_file(file_id=file_id)

    return {"message": "Deleted successfully"}