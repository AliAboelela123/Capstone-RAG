import os
import uuid
import PyPDF2 
import openai
from serverLLM.config import OPEN_AI_API_KEY
from sklearn.metrics.pairwise import cosine_similarity

os.environ["OPENAI_API_KEY"] = OPEN_AI_API_KEY

vector_index = []
text_index = {}

def get_embedding(chunk):
    # OpenAI's API expects a list of texts
    response = openai.Embedding.create(
        input=[chunk],
        model="text-embedding-ada-002"  # Replace with your desired model
    )
    # Extract embedding from the response
    embedding = response['data'][0]['embedding']
    return embedding

def pdf_to_text(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text_list = []
        for page_num in range(reader.numPages):
            text_list.append(reader.getPage(page_num).extractText())
            
    return text_list

def store_embeddings(file_path):
    if file_path is None:
        return False

    # Load the PDF and split it into pages
    string_chunks = pdf_to_text(file_path)
    # Get embedding model
    for chunk in string_chunks:
        random_uuid = str(uuid.uuid4())
        print("the random uuid is: ", random_uuid)
        text_index[random_uuid] = chunk
        chunk_embedding = get_embedding(chunk)
        vector_index.append((random_uuid, chunk_embedding))
    
    return True

def get_best_chunks(query):
    query_vector = get_embedding(query)
    #create a vector of uuids in the same order as the vector_index
    uuid_vector = []
    embedding_vector = []
    for uuid, embedding in vector_index:
        uuid_vector.append(uuid)
        embedding_vector.append(embedding)  
    #calculate cosine similarity
    cosine_sim = cosine_similarity([query_vector], embedding_vector)
    #find the index of the highest cosine similarity
    max_index = cosine_sim.argmax()
    #get the uuid of the highest cosine similarity
    best_uuid = uuid_vector[max_index]
    #get the text of the highest cosine similarity
    best_text = text_index[best_uuid]
    return best_text
        




    


    