# backend/services/file_parser.py
import PyPDF2
import docx
from typing import IO

class FileParser:
    @staticmethod
    def parse(file: IO, file_type: str) -> str:
        """
        Parses a file-like object based on its content type and returns extracted text.
        
        :param file: A file-like object (from open(path, 'rb')).
        :param file_type: The MIME type of the file (e.g., 'application/pdf').
        :return: Extracted text as a single string.
        """
        text = ""
        if file_type == 'application/pdf':
            try:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() or ""
            except Exception as e:
                print(f"Error parsing PDF: {e}")
                # Optionally return a specific error message or raise
                return "Error: Could not parse PDF file."
        
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            try:
                doc = docx.Document(file)
                for para in doc.paragraphs:
                    text += para.text + "\n"
            except Exception as e:
                print(f"Error parsing DOCX: {e}")
                return "Error: Could not parse DOCX file."

        elif file_type == 'text/plain':
            try:
                # Assuming the file-like object was opened in binary, we need to decode
                text = file.read().decode('utf-8')
            except Exception as e:
                print(f"Error parsing TXT: {e}")
                return "Error: Could not parse text file."
        else:
            print(f"Unsupported file type: {file_type}")
            return f"Error: Unsupported file type '{file_type}'."
            
        return text.strip()