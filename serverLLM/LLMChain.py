import openai
from langchain.chat_models import ChatOpenAI

from config import OPEN_AI_API_KEY

# LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0, openai_api_key=OPEN_AI_API_KEY,streaming=True,verbose=True)
chat_history = []

def construct_prompt(system_msg, context_msg, question):
    """
    Constructs the Chat Prompt with System Messages, Context, and the User Question,
    Including a Dynamically Calculated Portion of the Chat History.
    """
    print(context_msg)
    # Calculate Word Count for Fixed Inputs
    fixed_parts_word_count = len(system_msg.split()) + len(context_msg.split()) + len(question.split())
    remaining_word_budget = 3500 - fixed_parts_word_count

    # Determine the # of Chat Entries to Consider
    num_entries_to_consider = min(len(chat_history), 10)

    # Calculate Words Per Entry
    words_per_entry = max(remaining_word_budget // max(num_entries_to_consider, 1), 1)

    # Process Chat History
    processed_chat_history = []
    for entry in chat_history[-num_entries_to_consider:]:
        entry_words = entry.split()
        processed_entry = " ".join(entry_words[:words_per_entry])
        processed_chat_history.append(processed_entry)

    # Combine Prompt and Return
    prompt_parts = [
        f"System Message: {system_msg}\n",
        f"Context Message: {context_msg}\n" if context_msg else "",
        f"Question: {question}\n",
        "Chat History:\n" + "\n".join(processed_chat_history),
    ]
    return "\n".join(prompt_parts)

def get_response(query, complexity, text_chunks=None, table_chunks=None):
    print("Prompting the LLM")
    system_msg = f"You are a friendly chatbot having a conversation with a human. You are an expert in finance and specifically trained on 10K data from Top 50 companies in 2022 and 2023. The user you are speaking with has a {complexity} understanding of finance."
    
    context_msg = ""
    if text_chunks:
        context_msg = "The user has uploaded a PDF document which has been parsed where relevant excerpt(s) from the document have been provided. It may assist you with the user's next question. \n<START_EXCERPT>\n" + "\n\n".join(
            [f"<CHUNK {i}> {text_chunk.text}" for i, text_chunk in enumerate(text_chunks)]) + "\n<END_OF_EXCERPTS>\n"
    
    if table_chunks:
        context_msg += "\n The following table(s) extracted from the document may be relevant to the user query\n"
        context_msg.join([f"<Table {i}> \n {table_chunk.text}" for i, table_chunk in enumerate(table_chunks)]) + "\n<END_OF_TABLES>"

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
        
        # Adds Chunk Sizing and Streaming
        for chunk in response:
            if 'choices' in chunk and len(chunk['choices']) > 0 and 'content' in chunk['choices'][0]['delta']:
                yield chunk['choices'][0]['delta']['content']
            if 'choices' in chunk and len(chunk['choices']) > 0 and 'finish_reason' in chunk['choices'][0]['delta']:
                break

    except Exception as e:
        print(f"An Error Occurred: {e}")
        yield "I'm sorry, but I couldn't generate a response, please check the PDFs uploaded and your query and try again. Thanks!"