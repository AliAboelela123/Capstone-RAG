from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import openai
from langchain.chains import LLMChain # Library for facilitating conversations
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory 
from config import OPEN_AI_API_KEY

# LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0, openai_api_key=OPEN_AI_API_KEY,streaming=True,verbose=True)
chat_history = []

# Prompt: Anytime a query is made, a prompt is constructed which contains more than just the query itself
# prompt = ChatPromptTemplate(
#     input_variables=[
#         "system_msg",
#         "chat_history",
#         "question"
#     ],
#     messages=[
#         # This system message will appear in any prompt, every time
#         SystemMessagePromptTemplate.from_template("{system_msg}"),
#         # The `variable_name` here is what must align with memory. This here will be the chat history.
#         MessagesPlaceholder(variable_name="chat_history"),
#         # Since we use {} we define a variable. This variable represents any system messages we might want to modify mid session
#         SystemMessagePromptTemplate.from_template("{context}"),
#         # Since we use {} we define a variable. This variable represents the user's query.
#         HumanMessagePromptTemplate.from_template("{question}")
#     ]
# )

# # Notice that we `return_messages=True` to fit into the MessagesPlaceholder
# # Notice that `"chat_history"` aligns with the MessagesPlaceholder name
# memory = ConversationBufferMemory(memory_key="chat_history", input_key="question", return_messages=True)
# conversation = LLMChain(
#     llm=llm,
#     prompt=prompt,
#     verbose=True,
#     memory=memory
# )


# def get_response(query, complexity, context=None):
#     system_msg = f"You are a friendly chatbot having a conversation with a human. You are an expert in finance. The user you are speaking with has a {complexity} understanding of finance."

#     context_msg = ""
#     if context:
#         context_msg += "The user has uploaded a document. Relevant excerpt(s) from the document have been provided. It may assist you with the user's next question. When a document is uploaded please enclose references from the user uploaded documents like so: <<reference>>:\n<START_EXCERPT>\n"
#         for i, chunk in enumerate(context):
#             context_msg += f"<CHUNK {i}> {chunk} \n\n"
#         context_msg += "<END_OF_EXCERPTS>"


#     input_data = {
#         "question": query,
#         "system_msg": system_msg,
#         "context": context_msg or "No Document Provided."
#     }

#     try:
#         print(conversation.generate([input_data]))
#         for part in conversation.generate([input_data]):  # Assume generate expects a list of inputs
#             if isinstance(part, dict):
#                 yield part['text'] + '\n\n'  # Correctly handle dictionary output
#             else:
#                 print(f"Unexpected output format: {part}")
#                 # Handle unexpected output format here (e.g., log it or convert it to a string if possible)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         # Handle other exceptions appropriately here

#     return input_data.get("text") or "I'm sorry, but I couldn't generate a response. Please check the inputs and try again."

def construct_prompt(system_msg, context_msg, question):
    """
    Constructs the chat prompt with system messages, context, and the user question.
    """
    prompt_parts = [
        f"{system_msg}\n",
        "\n".join(chat_history),
        f"{context_msg}\n" if context_msg else "",
        f"{question}\n"
    ]
    return "\n".join(prompt_parts)

def get_response(query, complexity, context=None):
    system_msg = f"You are a friendly chatbot having a conversation with a human. You are an expert in finance and specifically trained on 10K data from Top 50 companies in 2022 and 2023. The user you are speaking with has a {complexity} understanding of finance."
    
    context_msg = ""
    if context:
        context_msg = "The user has uploaded a PDF document which has been parsed where relevant excerpt(s) from the document have been provided. It may assist you with the user's next question. When a document is uploaded please enclose references from the user uploaded documents like so: <<reference>>:\n<START_EXCERPT>\n" + "\n\n".join(
            [f"<CHUNK {i}> {chunk}" for i, chunk in enumerate(context)]) + "\n<END_OF_EXCERPTS>"
    
    prompt = construct_prompt(system_msg, context_msg, query)
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            stream=True
        )
        
        for chunk in response:
            if 'choices' in chunk and len(chunk['choices']) > 0 and 'content' in chunk['choices'][0]['delta']:
                yield chunk['choices'][0]['delta']['content']
            if 'choices' in chunk and len(chunk['choices']) > 0 and 'finish_reason' in chunk['choices'][0]['delta']:
                break  # End the loop if 'finish_reason' is present, indicating the end of the stream

    except Exception as e:
        print(f"An error occurred: {e}")
        yield "I'm sorry, but I couldn't generate a response. Please check the inputs and try again."