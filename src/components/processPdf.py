import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from src.entity.config import ProcessingConfig
from src.entity.artifacts import IngestArtifact, ProcessingArtifact
from src.services.model_service import get_embedding_model

class ProcessPdfToVector:
    def __init__(self, ingest_artifact: IngestArtifact, config: ProcessingConfig):
        self.ingestion_artifact = ingest_artifact
        self.config = config
        # self.model = SentenceTransformer(self.config.embedding_model_name)
        # os.makedirs(config.faiss_dir_path,exist_ok=True)
        # os.makedirs(config.metadata_dir_path,exist_ok=True)
        self.embedding = get_embedding_model(model_name=self.config.embedding_model_name)

        self.chroma_client = chromadb.PersistentClient(path=self.config.chroma_db_path)
    
    # def _create_embedding(self, chunk_file_path, metadata_file_path):
    #     with open(chunk_file_path, "r", encoding="utf-8") as f:
    #         chunks = json.load(f)

    #     # Add IDs
    #     for i, chunk in enumerate(chunks):
    #         chunk["id"] = i

    #     texts = [chunk["text"] for chunk in chunks]

    #     print("🔄 Creating embeddings...")
    #     embeddings = self.model.encode(
    #         texts,
    #         show_progress_bar=True,
    #         normalize_embeddings=True
    #     )

    #     with open(metadata_file_path, "w", encoding="utf-8") as f:
    #         json.dump(chunks, f, indent=2, ensure_ascii=False)

    #     return embeddings

    # def _create_faiss(self, embeddings, faiss_file_path):
    #     embeddings = np.array(embeddings).astype("float32")

    #     dimension = embeddings.shape[1]
    #     index = faiss.IndexFlatL2(dimension)
    #     index.add(embeddings)

    #     faiss.write_index(index, faiss_file_path)

    #     return faiss_file_path

    def processPdf(self):
        # metadata_path = os.path.join(
        #     self.config.metadata_dir_path,
        #     self.config.metadata_file_name
        # )

        # faiss_path = os.path.join(
        #     self.config.faiss_dir_path,

        #     self.config.faiss_file_name
        # )

        # embeddings = self._create_embedding(
        #     self.ingestion_artifact.chunk_file_path,
        #     metadata_path
        # )

        # self._create_faiss(embeddings, faiss_path)

        with open(self.ingestion_artifact.chunk_file_path,"r",encoding="utf-8") as f:
            chunks = json.load(f)

        texts = [chunk["text"] for chunk in chunks]

        ## JUst dummy metadata logic to satisfy "Audit Trail" requirement
        metadatas = [{"source": chunk.get("source","finlens"), "page": chunk.get("page",0)} for chunk in chunks]
        ids = [f"id_{i}" for i in range(len(chunks))]

        print("Ingestion into ChromaDB (Persistent)....")

        ## Let's initialize/Get collection and add the document
        vector_store = Chroma(
            client=self.chroma_client,
            collection_name="finlens_collection",
            embedding_function=self.embedding
        )

        vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)

        return ProcessingArtifact(
            chroma_db_path=self.config.chroma_db_path,
            collection_name= "finlens_collection"
        )
