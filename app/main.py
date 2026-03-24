from fastapi import FastAPI
from app.api.routes import router


app = FastAPI(
    title="Discusso ML Service",
    version="0.1.0"
)

app.include_router(router=router)

## uvicorn app.main:app --reload
