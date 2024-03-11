# Standard Library Imports
import os
import uuid

# Related Third Party Imports
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import openai

# Local Application/Library Specific Imports
from config import OPEN_AI_API_KEY, TOKEN_COUNT, ALGORITHM, NUM_CHUNKS
from chunk import Chunk
from utilities import pdf_to_text

# Setting OpenAI API Key from Environment Variable
os.environ["OPENAI_API_KEY"] = OPEN_AI_API_KEY

# Stores Texts: A Dictionary with Embedding_ID as Key and Text as Value
text_db = {}
# Stores tables
tables_db = {}

def get_embedding(chunk):
    # Ensures the Chunk Is a String and Not Empty
    if not isinstance(chunk, str) or not chunk.strip():
        raise ValueError("Chunk Must Be a Non-Empty String")
    try:
        # OpenAI's API Expects a List of Texts
        openai.api_key = OPEN_AI_API_KEY
        response = openai.Embedding.create(
            input=[chunk],
            model="text-embedding-ada-002"
        )
        # Extract Embedding from the Response
        embedding = response['data'][0]['embedding']
        return embedding
    except openai.APIError as e:
        print("Invalid Request to OpenAI API:", e)
        raise
    except Exception as e:
        print("An Exception Occurred While Getting Embeddings:", e)
        raise


def store_tables(directory, num_files, source):
    print("Entered store table function")

    # Converts CSV Files to chunks then Deletes Them
    for i in range(num_files):
        # Create File Path
        file_path = os.path.join(directory, f"table_{i}.csv")
        print(file_path)
        if os.path.exists(file_path):
            
            try:
                # Open the file
                df = pd.read_csv(file_path)
                # Create & insert the chunk
                csv_string = df.to_csv(index=False, sep='\t') + "\n"
                table_embedding = get_embedding(csv_string)
                uuid_value = str(uuid.uuid4())
                tables_db[uuid_value] = Chunk(uuid_value, csv_string, table_embedding, source)
                # Delete the CSV file
                os.remove(file_path)
                print(f"Deleted File: {file_path}")
            except Exception as e:
                print(f"Error Deleting File {file_path}: {e}")
        else:
            print(f"File Not Found: {file_path}")
    
    print("Exited store table function")
    return True


def store_text(file_path, source):
    print("Entered store text function")
    # Converts CSV Files to a Single String and Deletes Them
    if file_path is None:
        return False

    print("Entered pdf to text")
    # Load the PDF and Split it into Pages
    string_chunks = pdf_to_text(file_path)

    # Get Embedding Model
    for chunk in string_chunks:
        if not chunk.strip():
            print("Skipping Empty Chunk")
            continue
        try:
            uuid_value = str(uuid.uuid4())
            chunk_embedding = get_embedding(chunk)
            text_db[uuid_value] = Chunk(uuid_value, chunk, chunk_embedding, source)
        except ValueError as e:
            print(f"Skipping Chunk Due to Error: {e}")
        except Exception as e:
            print(f"An Exception Occurred While Processing Chunk: {e}")

    print("Exit store text function")
    return True


def greedy_algorithm(similarities_dict, num_chunks):
    # Selects Top Chunks Based on Cosine Similarity Scores
    if num_chunks <= 0:
        return []

    # Sort the Dictionary by Similarity Scores in Descending Order
    sorted_similarity_items = sorted(similarities_dict.items(), key=lambda x: x[1], reverse=True)

    # Extract the embedding_ids of the Top num_chunks Chunks
    top_chunks = [embedding_id for embedding_id, _ in sorted_similarity_items[:num_chunks]]

    return top_chunks


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def probabilistic_algorithm(similarities_dict, num_chunks):
    # Selects Chunks Based on Probabilities Derived from Cosine Similarities
    if num_chunks <= 0:
        return []

    # Convert Cosine Similarities to Probabilities Using Softmax
    similarities_values = list(similarities_dict.values())
    probabilities = softmax(similarities_values)

    selected_chunks = []

    for _ in range(num_chunks):
        if probabilities.size == 0:
            break

        # Roll the Dice to Select an embedding_id Based on Probabilities
        selected_index = np.random.choice(len(probabilities), p=probabilities)

        # Get the Corresponding embedding_id
        selected_embedding_id = list(similarities_dict.keys())[selected_index]
        
        # Remove the Selected embedding_id and its Probability from the Lists
        del similarities_dict[selected_embedding_id]
        probabilities = softmax(list(similarities_dict.values()))

        # Add the selected_embedding_id to the List of Selected Chunks
        selected_chunks.append(selected_embedding_id)

    return selected_chunks

# TODO: Specify Params like Algorithm, Chunks, Chunk Size

def get_best_chunks(query, algorithm=ALGORITHM, num_chunks=NUM_CHUNKS):
    print("Calculating best chunks")
    # Selects Chunks based on Cosine Similarities
    query_vector = get_embedding(query)

    # Ensure query_vector is a 2D Array Before cosine_similarity
    data_array = np.array(query_vector)
    query_vector = data_array.reshape(1, -1)

    # Extract the List of Vectors and UUIDs from the vector_index
    text_embeddings = [Chunk.embedding for _, Chunk in text_db.items()]
    text_uuids = [text_uuid for text_uuid, _ in text_db.items()]

    table_embeddings = [Chunk.embedding for _, Chunk in tables_db.items()]
    table_uuids = [table_uuid for table_uuid, _ in tables_db.items()]

    # Compute Cosine Similarities
    text_similarities = cosine_similarity(query_vector, text_embeddings)
    table_similarities = cosine_similarity(query_vector, table_embeddings)

    # Create a Dictionary to Associate UUIDs with Cosine Similarities
    text_similarities_dict = {uuid: similarity for uuid, similarity in zip(text_uuids, text_similarities[0])}
    table_similarities_dict = {uuid: similarity for uuid, similarity in zip(table_uuids, table_similarities[0])}

    best_text_uuids = []
    best_table_uuids = []

    try:
        if algorithm == 'G':
            best_text_uuids = greedy_algorithm(text_similarities_dict, num_chunks)
            best_table_uuids = greedy_algorithm(table_similarities_dict, num_chunks)
        elif algorithm == 'P':
            best_text_uuids = probabilistic_algorithm(text_similarities_dict, num_chunks)
            best_table_uuids = probabilistic_algorithm(table_similarities_dict, num_chunks)
    except ValueError as e:
        print(f"An Exception Occurred While Getting Best Chunk: {e}")
        return "An Error Occurred While Processing the Documents. Please Try Again."

    print("Done finding best chunks")
    return [text_db[uuid] for uuid in best_text_uuids], [tables_db[uuid] for uuid in best_table_uuids]
