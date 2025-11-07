from typing import List, Dict
import chromadb
from chromadb.utils import embedding_functions

class NephroRAG:
    def __init__(self, path="app/rag/store"):
        self.client = chromadb.PersistentClient(path=path)
        self.coll = self.client.get_or_create_collection(
            name="nephro",
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        )

    def search(self, query:str, k:int=4) -> List[Dict]:
        res = self.coll.query(query_texts=[query], n_results=k)
        docs = res["documents"][0]
        metas = res["metadatas"][0]
        return [{"text":d, "source":m.get("source"), "page_hint":m.get("page_hint")} for d,m in zip(docs,metas)]
