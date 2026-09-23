from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import time
import os
from config import PDF_PATH, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL, COLLECTION_NAME
from jina_embeddings import JinaEmbeddings
from dotenv import load_dotenv

load_dotenv()


data = PyPDFLoader(str(PDF_PATH))

docs= data.load()


splite = RecursiveCharacterTextSplitter(
    chunk_size= CHUNK_SIZE,
    chunk_overlap= CHUNK_OVERLAP
)

final_splite = splite.split_documents(documents=docs)

emb= JinaEmbeddings(
    model= EMBEDDING_MODEL
)



vector= Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory="Chorma_db",
    embedding_function=emb
)


vector.add_documents(final_splite)
