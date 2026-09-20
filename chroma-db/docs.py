from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
from langchain_chroma import Chroma
from pathlib import Path
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

pdf_path = BASE_DIR / "jd_dataset" / "tech_jds_149.pdf"

chroma_path = BASE_DIR / "Vector-db"


loader = PyPDFLoader(str(pdf_path))

docs = loader.load()



model = GoogleGenerativeAIEmbeddings(
    model= 'gemini-embedding-001'
)


splitter= RecursiveCharacterTextSplitter(
    chunk_size= 800,
    chunk_overlap= 100
)

fin_splitter= splitter.split_documents(documents=docs)

print("Original pages:", len(docs))
print("Total chunks:", len(fin_splitter))


vector_db = Chroma(
    collection_name="fin_splitter",
    embedding_function= model,
    persist_directory=str(chroma_path)
)



BATCH_SIZE = 20

total = len(fin_splitter)

for start in range(0, total, BATCH_SIZE):
    end = min(start + BATCH_SIZE, total)

    batch = fin_splitter[start:end]

    print(f"Embedding chunks {start + 1} → {end} / {total}")

    vector_db.add_documents(batch)

    print(f" Stored {len(batch)} chunks")

    # Give Gemini time before the next batch
    if end < total:
        print(" Waiting 10 seconds...")
        time.sleep(10)

print("\n All chunks stored successfully!")