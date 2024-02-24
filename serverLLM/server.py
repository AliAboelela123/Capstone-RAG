"""
Flask Server Module to Handle Requests and Provide LLM Responses.
"""

from flask import Flask, Response, jsonify, request, stream_with_context
from flask_cors import CORS
from waitress import serve
from werkzeug.utils import secure_filename
import os
import json

from LLMChain import get_response
from embeddings_db import get_best_chunks, store_embeddings, extractCsv, csvs_to_string_and_delete
from utilities import allowed_file


# Flask app setup
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Setup CORS
CORS(app)

ALLOWED_EXTENSIONS = {'pdf'}

current_directory = os.path.dirname(os.path.abspath(__file__))
upload_directory = os.path.join(current_directory, 'uploads')
if not os.path.exists(upload_directory):
    os.makedirs(upload_directory)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/hello')
def hello():
    """
    Test endpoint to check if the server is responding.
    """
    return jsonify({"message": "Hello world!"})

@app.route('/query', methods=['POST'])
def query_endpoint():
    try:
        query = request.form.get('query')
        complexity = request.form.get('complexity', 'Expert')
        if not query:
            return jsonify({'error': "No Query Provided."}), 400

        # Process PDF files and extract context
        pdf_files = process_pdf_files(request.files.getlist('pdfFiles') if 'pdfFiles' in request.files else [])

        print("Before context")
        # Assuming get_best_chunks and other utility functions are adapted to provide relevant context
        context = get_best_chunks(query)
        print("After context")

        def generate_responses():
            try:
                for response_part in get_response(query, complexity):
                    # Check if the response part is an error
                    if isinstance(response_part, dict) and response_part.get('error'):
                        yield f"data: {json.dumps({'data': response_part})}\n\n"
                        break
                    else:
                        yield json.dumps({'data': response_part}) + '\n\n'
            except Exception as e:
                # If an exception occurs, yield an error message (this part won't execute due to how generators work with exceptions)
                yield json.dumps({'error': str(e)}) + '\n\n'

        return Response(stream_with_context(generate_responses()), mimetype='application/json'), 200


    except Exception as e:
        return jsonify({'error': str(e)}), 500

def process_pdf_files(pdf_files):
    # Implement PDF processing, including storing embeddings and extracting contexts
    # This function should return a list or dictionary of processed PDF file paths or contexts
    processed_files = []
    for file in pdf_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_directory, filename)
            file.save(file_path)
            processed_files.append(file_path)
            print("Before extractCsv call")
            numFiles = extractCsv(file_path)
            print("After extractCsv call")
            print("Before csvs_to_string_and_delete call")
            csvString = csvs_to_string_and_delete("./", numFiles)
            print("After csvs_to_string_and_delete call")
            # Assuming store_embeddings function returns context
            print("Before store_embeddings call")
            store_embeddings(file_path, csvString)
            print("After store_embeddings call")
            # Debug print
            print("File Saved:", file_path)
    return processed_files


# @app.route('/query', methods=['POST'])
# def query_endpoint():
#     try:
#         query = request.form.get('query')
#         if not query:
#             return jsonify({'error': "No Query Provided."}), 400
#         complexity = request.form.get('complexity', 'Expert')
#         pdf_files = []
#         context = None

#         print("Files Received:", request.files)

#         # Check for PDF Files in the Request
#         if 'pdfFiles' in request.files:
#             files = request.files.getlist('pdfFiles')
#             for file in files:
#                 print("Processing File:", file.filename)
#                 #process the file
#                 if file and allowed_file(file.filename):
#                     filename = secure_filename(file.filename)
#                     file_path = os.path.join(upload_directory, filename)
#                     file.save(file_path)
#                     pdf_files.append(file_path)
#                     numFiles = extractCsv(file_path)
#                     csvString = csvs_to_string_and_delete("./", numFiles)
#                     # Assuming store_embeddings function returns context
#                     store_embeddings(file_path, csvString)
#                     # Debug print
#                     print("File Saved:", file_path)
        
#         context = get_best_chunks(query)

#         def generate_responses():
#             for response in get_response(query, complexity, context):
#                 yield response

#         # Stream the responses using stream_with_context
#         return Response(stream_with_context(generate_responses()), content_type='text/event-stream')

#         llm_response = get_response(query, complexity, context)

#         if llm_response:
#             return Response(stream_with_context(get_response(query, complexity, context)), mimetype='text/event-stream')
#             response_data = {'response': llm_response}
#             if pdf_files:
#                 response_data['files'] = [os.path.basename(f) for f in pdf_files]
#             return jsonify(response_data), 200
#         else:
#             return jsonify({'error': "No Response From the Language Model."}), 500
#     except Exception as e:
#         print(f"An Exception Occurred: {e}")
#         return jsonify({'error': str(e)}), 500


def start_server():
    """
    Start the Flask server with waitress as the production server.
    """
    serve(app, host='0.0.0.0', port=5001)


if __name__ == '__main__':
    start_server()
