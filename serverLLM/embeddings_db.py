import os
import uuid
import PyPDF2 
import openai
from config import OPEN_AI_API_KEY, TOKEN_COUNT, ALGORITHM, NUM_CHUNKS
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import fitz
import tabula
import pandas as pd

os.environ["OPENAI_API_KEY"] = OPEN_AI_API_KEY

# A list of pairs. (embedding_id, [embedding]). Stores embeddings in vector format.
vector_index = []

# A dictionary of strings. Key is embedding_id, and value is str/text.
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
    except openai.APIError as e:
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
    #Function to convert the CSV files into a string and then deletes the table.csv file to make room for the next file
    combined_csv_string = ""
    for i in range(num_files):
        #create file path
        file_path = os.path.join(directory, f"table_{i}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            combined_csv_string += df.to_csv(index=False, sep='\t') + "\n"

            # Delete the CSV file after converting it to a string
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"File not found: {file_path}")
    #print(combined_csv_string)
    #returns string of csvs combined into one string
    return combined_csv_string


def store_embeddings(file_path, extracted_tables=None):
    print("Attempting to store embeddings")
    if file_path is None:
        return False

    # Load the PDF and split it into pages
    string_chunks = pdf_to_text(file_path)

    # Add the additional CSV text to the string_chunks with a contextual message
    if extracted_tables:
        csv_intro_message = "Here are the tables of the PDF in CSV format:\n"
        combined_csv_text = csv_intro_message + extracted_tables
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

def greedy_algorithm(similarities_dict, num_chunks):
    if num_chunks <= 0:
        return []

    # Sort the dictionary by similarity scores in descending order
    sorted_similarity_items = sorted(similarities_dict.items(), key=lambda x: x[1], reverse=True)

    # Extract the embedding_ids of the top num_chunks chunks
    top_chunks = [embedding_id for embedding_id, _ in sorted_similarity_items[:num_chunks]]

    return top_chunks


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def probabilistic_algorithm(similarities_dict, num_chunks):
    if num_chunks <= 0:
        return []

    # Convert cosine similarities to probabilities using softmax
    similarities_values = list(similarities_dict.values())
    probabilities = softmax(similarities_values)
    print("Probabilities")
    summm = 0
    for i in probabilities:
        print(i)
        summm+=i
    print(summm)
    selected_chunks = []

    for _ in range(num_chunks):
        if probabilities.size == 0:
            break  # Break if no more chunks available

        # Roll the dice to select an embedding_id based on probabilities
        selected_index = np.random.choice(len(probabilities), p=probabilities)

        # Get the corresponding embedding_id
        selected_embedding_id = list(similarities_dict.keys())[selected_index]
        
        # Remove the selected embedding_id and its probability from the lists
        del similarities_dict[selected_embedding_id]
        probabilities = softmax(list(similarities_dict.values()))

        # Add the selected_embedding_id to the list of selected chunks
        selected_chunks.append(selected_embedding_id)

    return selected_chunks

# TODO: Figure out how exactly we want to specify params like algorithm, chunks, chunk size, etc.
def get_best_chunks(query, algorithm=ALGORITHM, num_chunks=NUM_CHUNKS):
    query_vector = get_embedding(query)
    # Ensure query_vector is a 2D array before using it with cosine_similarity
    data_array = np.array(query_vector)
    query_vector = data_array.reshape(1, -1)  # Reshape for a single sample

    # Extract the list of vectors and UUIDs from the vector_index
    context_vectors = [embedding[1] for embedding in vector_index]
    uuids = [embedding[0] for embedding in vector_index]

    # Compute cosine similarities
    similarities = cosine_similarity(query_vector, context_vectors)

    # Create a dictionary to associate UUIDs with cosine similarities
    similarities_dict = {uuid: similarity for uuid, similarity in zip(uuids, similarities[0])}

    try:
        if algorithm == 'G':
            print("Greedy algorithm")
            best_chunk_uuids = greedy_algorithm(similarities_dict, num_chunks)
        elif algorithm == 'P':
            print("Probabilistic algorithm")
            best_chunk_uuids = probabilistic_algorithm(similarities_dict, num_chunks)
    except ValueError as e:
        print(f"An Exception Occurred while getting best chunk: {e}")
        return "An Error Occurred While Processing the Documents."

    return [text_index[i] for i in best_chunk_uuids]
