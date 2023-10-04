import subprocess
import multiprocessing
import webbrowser
import server

def run_server():
    server.start_server() # Call the server script

def run_app():
    # Python code to run "npm start" or whatever the command is to run the react app
    #webbrowser.open_new_tab('http://localhost:5000')
    pass

if __name__ == '__main__':
    # The flask server & react app are blocking processes, so we must use the multiprocessing library

    # First we open the browser to where the React app will be
    webbrowser.open_new_tab('http://localhost:5000')
    
    # Bind the first process to the run_server function
    server_process = multiprocessing.Process(target=run_server)
    
    # Bind the second process to the run_app function
    app_process = multiprocessing.Process(target=run_app)

    # Start the server & app process
    server_process.start()
    app_process.start()

    server_process.join()
    app_process.join()
    