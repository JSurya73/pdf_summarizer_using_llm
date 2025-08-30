import os
import json
from typing import List

# Packages for Data Loader, Preprocessing ,Embeddings, Vector DB store
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def build_or_load_vectorstore(pdf_path: str, faiss_dir: str = "faiss_index") -> FAISS:
    # if os.path.isdir(faiss_dir):
    #     # Load existing FAISS index
    #     vs = FAISS.load_local(faiss_dir, embeddings=HuggingFaceEmbeddings())
    #     return vs
    
    loader = PyPDFLoader(pdf_path)

    # Dtype: List[Document]
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 150,
        add_start_index = True,
        separators = ["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(docs)

    embed_model = "sentence-transformers/all-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name = embed_model)

    vs = FAISS.from_documents(chunks,embeddings)
    # vs.save_local(faiss_dir)

    return vs,embed_model