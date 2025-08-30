import os
import json
import base64
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from rag_components.rag_agent import *

# Packages for Data Loader, Preprocessing ,Embeddings, Vector DB store
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

app = Flask(__name__, instance_relative_config=True)
CORS(app)

# with open("../utils/credentials.json") as f:
#     credentials = json.load(f)
# os.environ["GROQ_API_KEY"] = credentials['Groq']['API_Key']

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/llmcall', methods=['POST'])
def llm_call():
    try:
        os.environ['GROQ_API_KEY'] = "your_api_key_here"

        data = request.get_json(force=True)
        vs_b64 = data['vector_store_b64']
        embed_model = data['metadata']['embedding_model']

        raw = base64.b64decode(vs_b64)
        embeddings = HuggingFaceEmbeddings(model_name = embed_model)
        vs = FAISS.deserialize_from_bytes(raw,embeddings,allow_dangerous_deserialization=True)

        chain = build_rag_chain(vs)
        answer = chain.invoke(input=data['query'])

        return jsonify({
            "query":data['query'],
            "answer":answer
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True,port=2001)

