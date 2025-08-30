import os
import json
from colorama import init, Fore
from typing import List

from langchain_community.vectorstores import FAISS

# Packages for LLM model, Prompt + RAG chain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def build_rag_chain(vs: FAISS):
    retriever = vs.as_retriever(search_type = "similarity", search_kwgs = {"k":4})

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
        max_tokens=None,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",
             "You are a helpful assistant for question answering over a provided document. "
             "Use ONLY the given context to answer. If the answer isn't in the context, say you don't know."),
            ("human",
             "Question: {question}\n\nContext:\n{context}\n\nAnswer:")
        ]
    )

    def format_docs(docs: List[Document]) -> str:
        # include source metadata for traceability
        return "\n\n---\n\n".join(
            f"[p{d.metadata.get('page', 'NA')}] {d.page_content.strip()}" for d in docs
        )

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain