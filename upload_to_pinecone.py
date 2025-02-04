import os
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI
import tiktoken
from typing import List

# Load environment variables
load_dotenv('.env.local')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index("phd-knowledge")

def get_encoding():
    """Get the encoding for the text."""
    return tiktoken.get_encoding("cl100k_base")  # This is the encoding used by text-embedding-ada-002

def split_text(text: str, chunk_size: int = 1000) -> List[str]:
    """Split text into chunks of approximately equal size."""
    encoding = get_encoding()
    tokens = encoding.encode(text)
    chunks = []
    
    current_chunk = []
    current_size = 0
    
    for token in tokens:
        current_chunk.append(token)
        current_size += 1
        
        if current_size >= chunk_size:
            # Decode the chunk back to text
            chunk_text = encoding.decode(current_chunk)
            chunks.append(chunk_text)
            current_chunk = []
            current_size = 0
    
    # Add any remaining text as the last chunk
    if current_chunk:
        chunk_text = encoding.decode(current_chunk)
        chunks.append(chunk_text)
    
    return chunks

def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Get embeddings for a list of texts using OpenAI's API."""
    embeddings = []
    for text in texts:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        embeddings.append(response.data[0].embedding)
    return embeddings

def upload_to_pinecone(file_path: str, namespace: str = "research"):
    """Upload a markdown file to Pinecone."""
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Split into chunks
    chunks = split_text(text)
    print(f"Split text into {len(chunks)} chunks")
    
    # Get embeddings
    embeddings = get_embeddings(chunks)
    print("Generated embeddings")
    
    # Prepare vectors for Pinecone
    vectors = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vectors.append({
            'id': f"{os.path.basename(file_path)}_chunk_{i}",
            'values': embedding,
            'metadata': {
                'text': chunk,
                'source': file_path,
                'chunk_index': i
            }
        })
    
    # Upload to Pinecone in batches
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch, namespace=namespace)
        print(f"Uploaded batch {i//batch_size + 1} of {(len(vectors)-1)//batch_size + 1}")

if __name__ == "__main__":
    file_path = "Innovation Ethics/articles/phil_article/proposal_ioai_analysis.md"
    upload_to_pinecone(file_path)  # Will use default "research" namespace
    print("Upload complete!") 