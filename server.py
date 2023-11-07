from flask import Flask, jsonify, request
from waitress import serve
from LLMChain import get_response
from embeddings_db import vector_database, store_embeddings

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, world!"

# This function will
# 1. 
@app.route('/query', methods=['POST'])
def query_endpoint():
    # Get the data from the request
    data = request.data.decode('utf-8')

    system_msg = get_best_chunks(query)
    vector_database.similarity_search(query)
    get_response(query, system_msg)

    # Example: Return the received data as JSON
    response = {'message': 'Received string:', 'data': data}
    return jsonify(response), 200

@app.route('/pdf-upload')
def get_pdf():
    # Ali's part
    pdf = request

    # Kevin's part
    store_embeddings(pdf)

def start_server():
    serve(app, host='127.0.0.1', port=5000)