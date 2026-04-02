from pydantic import BaseModel
from dataclasses import dataclass, field
from typing import List,Dict

@dataclass
class QueryResponse():
    answer: str
    sources: List[Dict] = field(default_factory=List)


class UploadPdfResponse(BaseModel):
    status: int
    file_id: str
    message: str = ""
    error: str = ""