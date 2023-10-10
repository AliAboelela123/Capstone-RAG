from flask import Flask, jsonify
from waitress import serve

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, world!"

@app.route('/query', methods=['POST'])
def query_endpoint():
    # Get the data from the request
    data = request.data.decode('utf-8')

    # Your code to process the input string (data) goes here
    # You can perform any necessary operations on the 'data' variable

    # Example: You can simply return the received data as JSON
    response = {'message': 'Received string:', 'data': data}
    return jsonify(response), 200


def start_server():
    serve(app, host='127.0.0.1', port=5000)

if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=5000)