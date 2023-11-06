from flask import Flask, jsonify, request, session
from waitress import serve
from serverLLM.LLMChain import get_response
from serverLLM.embeddings_db import get_best_chunks
from serverLLM.utilities import allowed_file 

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/hello')
def hello():
    return "<h1>Hello world!"

@app.route('/complexity', methods=['POST'])
def set_complexity():
    try:
        print('A')
        data = request.get_json()
        print('B')
        if 'complexity' in data:
            print('C')
            session['complexity'] = data['complexity']
            print('E')
        else:
            print('D')
            session['complexity'] = 'intermediate'
        return jsonify({'message': 'success'}), 200
    except:
        print("An exception occurred")
        return jsonify({'message': "Error"}), 400

@app.route('/query', methods=['POST'])
def query_endpoint():
    # Get the data from the request
    try:
        data = request.get_json()
        query = data['query']
        complexity = session.get('complexity', 'intermediate')
        context = get_best_chunks(query)
        LLMresponse = get_response(query, complexity, context)
        # Example: Return the received data as JSON
        response = {'ChatResponse': LLMresponse}
        return jsonify(response), 200
    
    except:
        print("An exception occurred")
        return jsonify({'ChatResponse': "Error"}), 400

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files.get("file_upload") # Note to Nelson: The name of the input field for the file upload must match this

        if file and allowed_file(file.filename):
            # Kevin put your code here. The pdf is in the "file" object.
            # Ask ChatGPT "Flask request.files methods" to get more information on
            # how you can work with this file object

            return jsonify({'message': 'PDF file uploaded successfully'}), 200
        else:
            return jsonify({'error': 'Invalid file format (PDF required)'}), 400

    except Exception as e:
        return jsonify({'error': "Error"}), 500

def start_server():
    serve(app, host='127.0.0.1', port=5000)