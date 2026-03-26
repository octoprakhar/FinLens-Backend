from pydantic import BaseModel


class QueryRequest(BaseModel):
    file_id: str
    query: str
    debug: bool = False