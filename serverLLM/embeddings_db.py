import os
import uuid
import PyPDF2 
import openai
from config import OPEN_AI_API_KEY, TOKEN_COUNT
from sklearn.metrics.pairwise import cosine_similarity
import fitz
import tabula
import pandas as pd

os.environ["OPENAI_API_KEY"] = OPEN_AI_API_KEY

vector_index = []
text_index = {}

def get_embedding(chunk):
    # Ensure that the chunk is a string and not empty
    if not isinstance(chunk, str) or not chunk.strip():
        raise ValueError("Chunk Must Be a Non-Empty String")

    try:
        # OpenAI's API expects a list of texts
        openai.api_key = OPEN_AI_API_KEY
        response = openai.Embedding.create(
            input=[chunk],
            model="text-embedding-ada-002"
        )
        # Extract embedding from the response
        embedding = response['data'][0]['embedding']
        return embedding
    except openai.error.InvalidRequestError as e:
        print("Invalid Request to OpenAI API:", e)
        raise
    except Exception as e:
        print("An Exception Occurred While Getting Embeddings:", e)
        raise


def pdf_to_text(file_path, max_token_count=TOKEN_COUNT):
    text_chunks = []
    current_chunk_tokens = []

    with fitz.open(file_path) as doc:
        for page in doc:
            # Extract text from the page and split into tokens using space as delimiter
            page_tokens = page.get_text().split()
            for token in page_tokens:
                current_chunk_tokens.append(token)
                # If the current chunk reaches or exceeds the max_token_count, join and save it
                if len(current_chunk_tokens) >= max_token_count:
                    text_chunks.append(' '.join(current_chunk_tokens))
                    current_chunk_tokens = []  # Reset for the next chunk

    # Add any remaining tokens as a final chunk
    if current_chunk_tokens:
        text_chunks.append(' '.join(current_chunk_tokens))

    return text_chunks

def extractCsv(file_path):
    df_list = tabula.read_pdf(file_path, pages='all', multiple_tables=True)
    #convert to csv 
    for i, df in enumerate(df_list):
        #save to currect directory
        df.to_csv(f'./table_{i}.csv', index=False)

    print("Number of files is: ", len(df_list))
    #Return number of tables
    return len(df_list)

def csvs_to_string_and_delete(directory, num_files):
    combined_csv_string = ""
    for i in range(num_files):
        file_path = os.path.join(directory, f"table_{i}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            combined_csv_string += df.to_csv(index=False, sep='\t') + "\n"

            # Delete the CSV file after converting it to a string
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"File not found: {file_path}")
    print(combined_csv_string)
    return combined_csv_string


def store_embeddings(file_path, additional_text=None):
    if file_path is None:
        return False

    # Load the PDF and split it into pages
    string_chunks = pdf_to_text(file_path)

    # Add the additional CSV text to the string_chunks with a contextual message
    if additional_text:
        csv_intro_message = "Here are the tables of the PDF in CSV format:\n"
        combined_csv_text = csv_intro_message + additional_text
        string_chunks.append(combined_csv_text)

    # Get embedding model
    for chunk in string_chunks:
        if not chunk.strip():
            print("Skipping Empty Chunk")
            continue

        try:
            random_uuid = str(uuid.uuid4())
            text_index[random_uuid] = chunk
            chunk_embedding = get_embedding(chunk)
            vector_index.append((random_uuid, chunk_embedding))
        except ValueError as e:
            print(f"Skipping Chunk Due to Error: {e}")
        except Exception as e:
            print(f"An Exception Occurred While Processing Chunk: {e}")

    return True


def get_best_chunks(query):
    if not vector_index:
        return "No Documents Have been Uploaded or Processed for Similarity."

    query_vector = get_embedding(query)
    embedding_vector = [embedding for _, embedding in vector_index]

    if not isinstance(embedding_vector, list) or not embedding_vector:
        return "No Embeddings Found for the Documents."

    try:
        cosine_sim = cosine_similarity([query_vector], embedding_vector)
        max_index = cosine_sim.argmax()
        best_uuid = vector_index[max_index][0]
        best_text = text_index[best_uuid]
        return best_text
    except ValueError as e:
        print(f"An Exception Occurred While Computing Cosine Similarity: {e}")
        return "An Error Occurred While Processing the Documents."
