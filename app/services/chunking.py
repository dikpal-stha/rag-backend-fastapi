from typing import List
import re

# fixed size chunking method
def fixed_size_chunking(text:str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start = end - overlap
    
    return chunks

# Sentence-based chunking method
def sentence_based_chunking(text:str, chunk_size = 500, overlap: int = 20) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        
        else:
            chunks.append(current_chunk.strip())

            # Handle overlap
            if overlap < 0:
                last_words = current_chunk.split()[-overlap:]
                current_chunk = " ".join(last_words) + " " + sentence + " "
            else:
                current_chunk = sentence + " "
        
        # for leftover sentences
        if current_chunk:
            chunks.append(current_chunk.strip())
    
    return chunks




            






