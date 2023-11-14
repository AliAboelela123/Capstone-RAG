import multiprocessing
import subprocess
import serverLLM.server as server


def run_server():
    """
    Start the Backend Server and have CORS enabled.
    """
    server.start_server()


def run_app():
    """
    Start the Frontend Application.
    """
    subprocess.call(["npm", "start"],
                    cwd="FinancialClient/financial-analyzer-client")


if __name__ == '__main__':
    # Set Up and Start the Backend Server Process.
    server_process = multiprocessing.Process(target=run_server)

    # Set Up and Start the Frontend Application Process.
    app_process = multiprocessing.Process(target=run_app)

    server_process.start()
    app_process.start()

    server_process.join()
    app_process.join()
