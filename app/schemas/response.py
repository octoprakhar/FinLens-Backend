from pydantic import BaseModel
from dataclasses import dataclass
from typing import List,Dict

@dataclass
class QueryResponse():
    answer: str
    sources: List[Dict]


class UploadPdfResponse(BaseModel):
    status: int
    file_id: str
    message: str = ""
    error: str = ""