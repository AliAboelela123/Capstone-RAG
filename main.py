import subprocess
import webbrowser

if __name__ == '__main__':
    #subprocess.run(["npm", "start"], cwd="app") # This line runs the web app using "npm start"
    webbrowser.open_new_tab('http://localhost:5000') # Assuming this is where the react app would be hosted
    subprocess.run(["python", "server.py"]) # This line runs the server script