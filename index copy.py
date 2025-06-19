import os
import json
import fitz  # PyMuPDF


def get_all_pdf_files(folder):
    # Recursively find all PDF files in the given folder and subfolders
    pdf_files = []
    for root, _, files in os.walk(folder):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, filename))
    return pdf_files


# Path to the folder containing your PDF files
PDF_FOLDER = 'dae-pdfs'  # Make sure this folder exists and contains PDFs
# Name of the file where the index will be saved
INDEX_FILE = 'pdf_index.txt'


def extract_text_from_pdf(pdf_path):
    # Extracts all text from a single PDF file
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def index_pdfs(folder):
    # Indexes all PDF files in the specified folder and its subfolders
    index = []
    for root, _, files in os.walk(folder):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                path = os.path.join(root, filename)
                text = extract_text_from_pdf(path)
                relative_path = os.path.relpath(path, folder)
                index.append({'filename': relative_path, 'content': text})
    return index


def save_index(index, index_file):
    # Saves the index to a text file
    with open(index_file, 'w', encoding='utf-8') as f:
        for entry in index:
            f.write(f"Filename: {entry['filename']}\n")
            f.write(f"Content:\n{entry['content']}\n")
            f.write("=" * 40 + "\n")


if __name__ == "__main__":
    if not os.path.isdir(PDF_FOLDER):
        print(f"Error: The folder '{PDF_FOLDER}' does not exist.")
    else:
        index = index_pdfs(PDF_FOLDER)
        save_index(index, INDEX_FILE)
        # Save the index as a JSON file for structured, searchable storage
        json_index_file = 'pdf_index.json'
        with open(json_index_file, 'w', encoding='utf-8') as jf:
            json.dump(index, jf, ensure_ascii=False, indent=2)
        print(f"Indexed {len(index)} PDFs. Index saved to {INDEX_FILE} and {json_index_file}")