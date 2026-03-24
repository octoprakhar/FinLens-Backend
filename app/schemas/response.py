from pydantic import BaseModel

class QueryResponse(BaseModel):
    answer: str


class UploadPdfResponse(BaseModel):
    status: int
    file_id: str
    error: str = ""