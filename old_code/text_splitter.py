# backend/services/text_splitter.py
from typing import List

class TextSplitter:
    @staticmethod
    def split(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
        """
        Splits a long text into smaller chunks with a specified overlap.

        :param text: The input text string.
        :param chunk_size: The target size of each chunk (in characters).
        :param chunk_overlap: The number of characters to overlap between chunks.
        :return: A list of text chunks.
        """
        if not text:
            return []

        words = text.split()
        chunks = []
        current_chunk = []
        
        # This is a very basic word-based splitter. Character-based is often better.
        # Let's do a character-based one instead for better consistency.
        
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - chunk_overlap
            
        return chunks