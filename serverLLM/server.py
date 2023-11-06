"""
Flask server module to handle requests and provide LLM responses.
"""

from flask import Flask, jsonify, request, session
from flask_cors import CORS
from waitress import serve
from werkzeug.utils import secure_filename
import os

from serverLLM.LLMChain import get_response
from serverLLM.embeddings_db import get_best_chunks
from serverLLM.utilities import allowed_file

# Flask app setup
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Setup CORS
CORS(app)

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/hello')
def hello():
    """
    Test endpoint to check if the server is responding.
    """
    return jsonify({"message": "Hello world!"})


@app.route('/complexity', methods=['POST'])
def set_complexity():
    """
    Set the complexity level for the LLM responses.
    """
    try:
        data = request.get_json()
        complexity = data.get('complexity', 'intermediate')
        session['complexity'] = complexity
        return jsonify({'message': 'Complexity set successfully'}), 200
    except Exception as e:
        print(f"An exception occurred: {e}")
        return jsonify({'error': "An error occurred while setting complexity"}), 400


@app.route('/query', methods=['POST'])
def query_endpoint():
    """
    Endpoint to receive queries and provide LLM responses.
    """
    try:
        data = request.get_json()
        query = data['query']
        complexity_level = data['complexity']
        complexity = session.get('complexity', complexity_level)

        pdf_files = []
        if 'pdfFiles' in request.files:
            files = request.files.getlist('pdfFiles')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join('/path/to/upload/directory', filename))
                    pdf_files.append(filename)

        context = get_best_chunks(query)
        llm_response = get_response(query, complexity, context)
        
        print(f"Received LLM Response: {llm_response}")  # Log the LLM Response
        
        if llm_response:
            return jsonify({'response': llm_response}), 200
        else:
            print("No Response from LLMChain.")
            return jsonify({'error': "No Response from the Language Model."}), 500
    except Exception as e:
        print(f"An exception occurred: {e}")
        return jsonify({'error': "An Error Occurred While Processing the Query"}), 400

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    """
    Endpoint to upload and process PDF files.
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        if file and allowed_file(file.filename):
            # Processing code goes here

            return jsonify(
                {'message': 'PDF file uploaded and processed successfully'}), 200
        else:
            return jsonify({'error': 'Unsupported file format'}), 400
    except Exception as e:
        print(f"An exception occurred: {e}")
        return jsonify({'error': str(e)}), 500


def start_server():
    """
    Start the Flask server with waitress as the production server.
    """
    serve(app, host='127.0.0.1', port=5000)


if __name__ == '__main__':
    start_server()
