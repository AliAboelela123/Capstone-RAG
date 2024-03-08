from flask import Flask, Response, jsonify, request, stream_with_context
from flask_cors import CORS
from waitress import serve
from werkzeug.utils import secure_filename
import os
import json

from LLMChain import get_response
from embeddings_db import get_best_chunks, store_text, store_tables
from utilities import allowed_file, extractCsv


#global variable for csv string
combinedTables = ''

# Flask app setup

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Setup CORS for Handling Cross-Origin Requests
CORS(app)

# Define Allowed Extensions for File Uploads
ALLOWED_EXTENSIONS = {'pdf'}

# Set Up Upload Directory
current_directory = os.path.dirname(os.path.abspath(__file__))
upload_directory = os.path.join(current_directory, 'uploads')
if not os.path.exists(upload_directory):
    os.makedirs(upload_directory)


# Validate Uploaded Files
def allowed_file(filename):
    """Check If File Extension Is Allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Endpoint for Processing Queries
@app.route('/query', methods=['POST'])
def query_endpoint():
    """Handle Query Requests and Provide LLM Responses."""
    try:
        query = request.form.get('query')
        complexity = request.form.get('complexity', 'Expert')
        if not query:
            return jsonify({'error': "No Query Provided."}), 400

        complexity = request.form.get('complexity', 'Expert')
        pdf_files = []

        print("Files Received:", request.files)
        # Check for PDF Files in the Request
        if 'pdfFiles' in request.files:
            files = request.files.getlist('pdfFiles')
            for file in files:
                print("Processing File:", file.filename)
                #process the file
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(upload_directory, filename)
                    file.save(file_path)
                    pdf_files.append(file_path)
                    numFiles = extractCsv(file_path)
                    store_tables("./", numFiles, filename)
                    store_text(file_path, filename)
                    # Debug print
                    print("File Saved:", file_path)

        best_text_chunks, best_table_chunks = get_best_chunks(query)

        def generate_responses():
            """Stream Responses to the Client."""
            try:
                for response_part in get_response(query, complexity, best_text_chunks, best_table_chunks):
                    # Check if the Response Part Is an Error
                    if isinstance(response_part, dict) and response_part.get('error'):
                        yield f"data: {json.dumps({'data': response_part})}\n\n"
                        break
                    else:
                        yield json.dumps({'data': response_part}) + '\n\n'
            except Exception as e:
                # Yield an Error Message if an Exception Occurs
                yield json.dumps({'error': str(e)}) + '\n\n'

        # references = find_references(best_text_chunks, response)
        return Response(stream_with_context(generate_responses()), mimetype='application/json'), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Start the Server
def start_server():
    """Start the Flask Server with Waitress as the Production Server."""
    serve(app, host='0.0.0.0', port=5001)

# Main Entry Point
if __name__ == '__main__':
    start_server()
