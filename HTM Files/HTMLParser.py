import json
import os
from bs4 import BeautifulSoup
from datetime import datetime


def process_html_file(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        return "File not found."

    # Read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text from paragraphs and headers
    paragraphs = [p.get_text(separator='\n', strip=True) for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

    # Extract and format tables
    tables = []
    for table in soup.find_all('table'):
        rows = []
        for row in table.find_all('tr'):
            cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            rows.append(' | '.join(cells))
        tables.append('\n'.join(rows))

    # Combine paragraphs and tables
    combined_text = ' '.join(paragraphs + tables)

    # Create JSONL content
    jsonl_content = {
        "messages": [
            {"role": "system", "content": "You are a financial AI that is trained on the top 30 companies in the S&P500, specially their 10Q forms."},
            {"role": "user", "content": "For American Express, in 2023 Q3, what is its Quarterly Report?"},
            {"role": "assistant", "content": combined_text}
        ]
    }

    # Save to JSONL file
    jsonl_file_name = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    with open(jsonl_file_name, 'w', encoding='utf-8') as jsonl_file:
        json.dump(jsonl_content, jsonl_file)

    return f"Processed content saved to {jsonl_file_name}"

# Example usage
file_path = 'AMEX_HTML.html'
print(process_html_file(file_path))
