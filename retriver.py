from langchain_chroma import Chroma
from jina_embeddings import JinaEmbeddings

from config import EMBEDDING_MODEL, COLLECTION_NAME

emb = JinaEmbeddings(
    model= EMBEDDING_MODEL
)

vector= Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory="Chorma_db",
    embedding_function=emb
)


retriver = vector.as_retriever(
    search_type="mmr",
    search_kwargs={
        "fetch_k"   : 10,
        "k" : 5,
        "lambda_mult" : 0.5
    }
)


