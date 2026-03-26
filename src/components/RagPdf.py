import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from google import genai

from src.entity.config import RagConfig
from src.entity.artifacts import ProcessingArtifact
from src.services.model_service import get_embedding_model
from src.services.vector_store_service import get_vector_store

class RagPipeline():
    def __init__(self, processing_artifact: ProcessingArtifact, config: RagConfig,file_id:str):
        self.config = config
        self.processing_artifact = processing_artifact
        self.model = get_embedding_model(config.embedding_model_name)
        self.index, self.metadata = get_vector_store(
            file_id=file_id,
            faiss_path=processing_artifact.faiss_file_path,
            metadata_path=processing_artifact.metadata_file_path
        )
        self.client = genai.Client(api_key=config.gemini_api_key)
        

    ## REtrieve the closest vectors
    def _search(self,query:str, k:int=5):
        query_embedding = self.model.encode([query],normalize_embeddings=True)
        query_embedding = np.array(query_embedding).astype('float32')

        distances, indices = self.index.search(query_embedding,k)

        results = []

        for i in indices[0]:
            results.append(self.metadata[i])

        return results
    
    ## Getting context for citation
    def _build_context(self,chunks):
        context = ""
        for i, chunk in enumerate(chunks):
            context += f"[Source {i+1} | Page {chunk['page']}]\n"
            context += chunk["text"] + "\n\n"

        return context
    
    def answer_query(self,query):
        chunks = self._search(query)

        context = self._build_context(chunks)

        prompt = f"""
    You are a financial document assistant.

    Answer the question ONLY using the provided context.
    Do NOT use outside knowledge.

    Always include page references like (Page X).

    If the answer is not found, say: "Not found in document."

    Context:
    {context}

    Question:
    {query}

    Answer:
    """
    
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        ## FOrmatting the source, to give clean code
        sources = [
            {
                "page": chunk["page"],
                "text": chunk["text"]
            }
            for chunk in chunks
        ]

        return {
        "answer": response.text,
        "sources": sources
    }

    def retrieve_chunks(self, query: str, k: int = 10):
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding,k)

        results = []

        for idx, dist in zip(indices[0], distances[0]):
            chunk = self.metadata[idx]
            results.append({
                "text": chunk["text"],
                "page": chunk["page"],
                "score": float(dist)
            })

        return results

