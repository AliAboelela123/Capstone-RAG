from flask import Flask, jsonify, request
from waitress import serve

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, world!"

@app.route('/query', methods=['POST'])
def query_endpoint():
    # Get the data from the request
    try:
        data = request.data.decode('utf-8')
    except:
        print("An exception occurred")

    # Example: Return the received data as JSON
    response = {'message': 'Received string:', 'data': data}
    return jsonify(response), 200


def start_server():
    serve(app, host='127.0.0.1', port=5000)