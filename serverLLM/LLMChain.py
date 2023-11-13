from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain # Library for facilitating conversations
from langchain.chat_models import ChatOpenAI # The open AI model
from langchain.memory import ConversationBufferMemory # Giving our model memory of the chat history
from serverLLM.config import OPEN_AI_API_KEY

# LLM
llm = ChatOpenAI(temperature=0, openai_api_key=OPEN_AI_API_KEY)

# Prompt: Anytime a query is made, a prompt is constructed which contains more than just the query itself
prompt = ChatPromptTemplate(
    input_variables=[
        "system_msg",
        "chat_history",
        "question"
    ],
    messages=[
        # This system message will appear in any prompt, every time
        SystemMessagePromptTemplate.from_template("{system_msg}"),
        # The `variable_name` here is what must align with memory. This here will be the chat history.
        MessagesPlaceholder(variable_name="chat_history"),
        # Since we use {} we define a variable. This variable represents any system messages we might want to modify mid session
        SystemMessagePromptTemplate.from_template("{context}"),
        # Since we use {} we define a variable. This variable represents the user's query.
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)

# Notice that we `return_messages=True` to fit into the MessagesPlaceholder
# Notice that `"chat_history"` aligns with the MessagesPlaceholder name
memory = ConversationBufferMemory(memory_key="chat_history", input_key="question", return_messages=True)
conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
)


def get_response(query, complexity, context=None):
    system_msg = f"You are a friendly chatbot having a conversation with a human. You are an expert in finance. The user you are speaking with has a {complexity} understanding of finance."

    context_msg = ""
    if context:
        context_msg = "The user has uploaded a document. A relevant excerpt from the document has been provided. It may assist you with the user's next question: <START_EXCERPT>" + context + " <END_EXCERPT>"

    result = conversation({
        "question": query,
        "system_msg": system_msg,
        "context": context_msg or "No Document Provided."
    })

    return result.get("text") or "I'm sorry, but I couldn't generate a response. Please check the inputs and try again."
