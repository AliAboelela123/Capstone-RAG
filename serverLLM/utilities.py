import re
import tabula, fitz

from config import TOKEN_COUNT

def allowed_file(filename):
    return filename != '' and filename.lower().endswith('.pdf')

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
    print("Exit PDF to Text")
    return text_chunks


def extractCsv(file_path):
    print("Entering Extract CSV")
    # Extracts Tables from PDF as CSV
    df_list = tabula.read_pdf(file_path, pages='all', multiple_tables=True)
    # Convert to CSV 
    for i, df in enumerate(df_list):
        # Save to Currect Directory
        df.to_csv(f'./table_{i}.csv', index=False)

    print("Number of File is: ", len(df_list))
    # Return Number of Tables
    return len(df_list)

def str_to_int(num_str):
    # Remove commas from the string representation of the number
    num_str_no_commas = num_str.replace(',', '')
    # Convert the string to an integer
    num_int = int(num_str_no_commas)
    return num_int

def check_duplicate_reference(references, str_match):
    for ref in references:
        print("Current reference tuple:", ref)
        if ref[1] == str_match:
            return True
    return False

def find_references(text_chunks, response):
    # Regular Expression to Find All Numbers
    numbers = re.findall(r'\b\d{1,3}(?:,\d{3})*\b', response)
    # Filter Out Years
    non_year_numbers = [num for num in numbers if not ((num.startswith('19') or num.startswith('20')) and len(num) == 4) and (str_to_int(num)-31>0)]

    references = []

    for num in non_year_numbers:
        for chunk in text_chunks:
            if len(references) > 4:
                break
            if num in chunk.text:
                str_match = chunk.find_reference(num)
                if str_match == None:
                    continue
                if check_duplicate_reference(references, str_match):
                    continue
                references.append((num, str_match, chunk.source))
    return references
