import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        return text.strip()
    except Exception as e:
        raise Exception(f'Failed to extract text from PDF: {str(e)}')

def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        raise Exception(f'Failed to read text file: {str(e)}')

def extract_text(file_path, file_extension):
    if file_extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == 'txt':
        return extract_text_from_txt(file_path)
    else:
        raise Exception(f'Unsupported file type: {file_extension}')
