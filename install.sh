#!/bin/bash

# Exit Script if any Command Fails
set -e

# Check if Python & pip are Installed
command -v python3 &>/dev/null || { echo "Python 3 is Not Installed."; exit 1; }
command -v pip3 &>/dev/null || { echo "pip3 is Not Installed."; exit 1; }

# Install Python Dependencies from requirements.txt
pip3 install -r requirements.txt

pyinstaller --onefile --onefile \
            --hidden-import waitress \
            --hidden-import langchain \
            --hidden-import typing_extensions \
            --hidden-import pydantic \
            --hidden-import serverLLM.config \
            --hidden-import openai \
            --add-data '/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/langchain:langchain' \
            main.py

echo "Installation Complete. You can now run your Application."
