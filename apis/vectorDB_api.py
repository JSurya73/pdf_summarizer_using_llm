# app.py
import os
import base64
import tempfile
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from rag_components.vector_db import build_or_load_vectorstore

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')  # Serves the HTML page

@app.route('/upload', methods=['POST'])
def upload_file():
    def hello_func(pdf_path, temp_path):
        print(f"Processing PDF at: {pdf_path}")
        print(f"Storing vector DB in: {temp_path}")

    if 'pdf' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['pdf']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save uploaded PDF to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        file.save(temp_pdf.name)
        pdf_path = temp_pdf.name

    # Create a temp dir to store vector DB
    temp_vector_db_path = tempfile.mkdtemp()

    try:
        vs, embed_model = build_or_load_vectorstore(
            pdf_path=pdf_path,
            faiss_dir=temp_vector_db_path
        )
        raw = vs.serialize_to_bytes()
        vs_b64 = base64.b64encode(raw).decode("utf-8")

        # Optional: include some metadata for the receiver
        meta = {
            "embedding_model": embed_model,
            "index_size": getattr(vs.index, "ntotal", None),
            "faiss_dimension": getattr(vs.index, "d", None),
        }

    
        return jsonify({
            "message": "Vector DB created successfully",
            "pdf_path": pdf_path,
            "vector_db_path": temp_vector_db_path,
            "vector_store_b64":vs_b64,
            "metadata":meta
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,port=2000)
