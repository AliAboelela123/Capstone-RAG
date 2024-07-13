# FinancialDocumentLLMAssistant
This is our (Ali Aboelela, Nelson Lee, Kevin Sadigh) capstone project. It can be described generally as a web app which acts as wrapper for a fine tuned LLM. Its main goal is to take in (primarily) financial pdf documents &amp; user queries as input then output a response to said queries. Non finance queries are directed to a base version of the LLM.

Although outside the scope of our capstone project, afer graduating we hope to improve the model such that it's capable of processing STEM research papers & queries at high performance. 

# How to run the app (dev)
1. Clone the repo
2. Add a config.py file under FinancialDocumentAIAnalyzer/serverLLM. This file should define the open AI api key with: OPEN_AI_API_KEY = "Your-key-here". You should also specify TOKEN_COUNT and NUM_CHUNKS. Make sure TOKEN_COUNT * NUM_CHUNKS is < 3000. Also, specify algorithm using ALGORITHM = 'G' or 'P' for greedy or probabilistic.
3. Download docker desktop, and make sure docker is running
4. Run the command "docker-compose up --build". This will build the containers, and run them.
5. Alternatively you can build and run in separate steps with "docker-compose build" and "docker-compose up -d"
6. You can now visit the application at localhost:3000.
7. Run "docker-compose down" to take down the containers.
