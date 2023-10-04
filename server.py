import subprocess
from flask import Flask
from waitress import serve

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, world!"

if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=5000)