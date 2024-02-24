# Standard Library Imports
import os
import uuid

# Related Third Party Imports
import numpy as np
import pandas as pd
import fitz  # PyMuPDF
import tabula
from sklearn.metrics.pairwise import cosine_similarity
import openai

# Local Application/Library Specific Imports
from config import OPEN_AI_API_KEY, TOKEN_COUNT, ALGORITHM, NUM_CHUNKS

# Setting OpenAI API Key from Environment Variable
os.environ["OPENAI_API_KEY"] = OPEN_AI_API_KEY

# Stores Embeddings in Vector Format: A List of Pairs (Embedding_ID, [Embedding])
vector_index = []

# Stores Texts: A Dictionary with Embedding_ID as Key and Text as Value
text_index = {}


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


def pdf_to_text(file_path, max_token_count=TOKEN_COUNT):
    # Extracts Text from PDF and Splits It into Manageable Chunks.
    text_chunks = []
    current_chunk_tokens = []

    with fitz.open(file_path) as doc:
        for page in doc:
            # Extract Text from the Page and Split into Tokens using Space as Delimiter
            page_tokens = page.get_text().split()
            for token in page_tokens:
                current_chunk_tokens.append(token)
                # If the Current Chunk Reaches or Exceeds the max_token_count, Join and Save It
                if len(current_chunk_tokens) >= max_token_count:
                    text_chunks.append(' '.join(current_chunk_tokens))
                    current_chunk_tokens = []  # Reset for Next Chunk

    if current_chunk_tokens:
        text_chunks.append(' '.join(current_chunk_tokens))

    return text_chunks


def extractCsv(file_path):
    # Extracts Tables from PDF as CSV
    df_list = tabula.read_pdf(file_path, pages='all', multiple_tables=True)
    
    # Convert to CSV 
    for i, df in enumerate(df_list):
        # Save to Currect Directory
        df.to_csv(f'./table_{i}.csv', index=False)

    print("Number of File is: ", len(df_list))
    # Return Number of Tables
    return len(df_list)


def csvs_to_string_and_delete(directory, num_files):
    # Converts CSV Files to a Single String and Deletes Them
    combined_csv_string = ""

    for i in range(num_files):
        # Create File Path
        file_path = os.path.join(directory, f"table_{i}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            combined_csv_string += df.to_csv(index=False, sep='\t') + "\n"

            # Delete the CSV file
            os.remove(file_path)
            print(f"Deleted File: {file_path}")
        else:
            print(f"File Not Found: {file_path}")

    # Returns String of CSVs Combined into One String
    return combined_csv_string


def store_embeddings(file_path, extracted_tables=None):
    # Converts CSV Files to a Single String and Deletes Them
    if file_path is None:
        return False

    # Load the PDF and Split it into Pages
    string_chunks = pdf_to_text(file_path)

    # Add the Additional CSV Text to the string_chunks with a Contextual Message
    if extracted_tables:
        csv_intro_message = "Here are the tables of the PDF in CSV format:\n"
        combined_csv_text = csv_intro_message + extracted_tables
        string_chunks.append(combined_csv_text)

    # Get Embedding Model
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
    summm = 0
    for i in probabilities:
        summm += i
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
    # Selects Chunks Based on Probabilities Derived from Cosine Similarities

    query_vector = get_embedding(query)

    # Ensure query_vector is a 2D Array Before cosine_similarity
    data_array = np.array(query_vector)
    query_vector = data_array.reshape(1, -1)

    # Extract the List of Vectors and UUIDs from the vector_index
    context_vectors = [embedding[1] for embedding in vector_index]
    uuids = [embedding[0] for embedding in vector_index]

    # Compute Cosine Similarities
    similarities = cosine_similarity(query_vector, context_vectors)

    # Create a Dictionary to Associate UUIDs with Cosine Similarities
    similarities_dict = {uuid: similarity for uuid, similarity in zip(uuids, similarities[0])}

    try:
        if algorithm == 'G':
            best_chunk_uuids = greedy_algorithm(similarities_dict, num_chunks)
        elif algorithm == 'P':
            best_chunk_uuids = probabilistic_algorithm(similarities_dict, num_chunks)
    except ValueError as e:
        print(f"An Exception Occurred While Getting Best Chunk: {e}")
        return "An Error Occurred While Processing the Documents. Please Try Again."

    return [text_index[i] for i in best_chunk_uuids]
