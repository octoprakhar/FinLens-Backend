from fastapi import FastAPI
from app.api.routes import router
from src.services.model_service import get_embedding_model


app = FastAPI(
    title="Discusso ML Service",
    version="0.1.0"
)


@app.on_event("startup")
def load_models():
    get_embedding_model()

app.include_router(router=router)

## uvicorn app.main:app --reload
