import os
import pinecone
import openai
import glob
from pathlib import Path
import time
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv('.env.local')

# Get configuration from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT', 'aws/us-east-1')

if not all([OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME]):
    raise ValueError("Missing required environment variables. Please check your .env.local file.")

# Configure paths and constants
TEXTS_DIR = "Witt-Trans/sections/ch8/0_texts_mds_english"
CHUNK_SIZE = 1000  # characters per chunk, with overlap
BATCH_SIZE = 100  # Number of vectors per batch, adjusted based on dimension size
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize Pinecone client
print("Initializing Pinecone...")
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Connect to the existing Pinecone index
print(f"\nConnecting to index: {PINECONE_INDEX_NAME}")
index = pc.Index(PINECONE_INDEX_NAME)

def read_markdown_file(file_path):
    """Read a markdown file and return its content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def chunk_text(text, filename, chunk_size=CHUNK_SIZE, overlap=200):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        # If this is not the first chunk, start a bit earlier to create overlap
        actual_start = start if start == 0 else start - overlap
        # If this is not the last chunk, try to break at a paragraph or sentence
        if end < text_len:
            # Try to find a paragraph break
            next_break = text.find('\n\n', end)
            if next_break != -1 and next_break < end + 200:  # Look within reasonable distance
                end = next_break
            else:
                # Try to find a sentence break
                next_period = text.find('. ', end)
                if next_period != -1 and next_period < end + 100:
                    end = next_period + 1

        chunk = text[actual_start:end].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append({
                'text': chunk,
                'source': filename,
                'start_char': actual_start,
                'end_char': end
            })
        start = end

    return chunks

def embed_text(text: str) -> List[float]:
    """Convert text into an embedding vector using OpenAI's embedding endpoint."""
    response = openai.Embedding.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    embedding = response["data"][0]["embedding"]
    return embedding

def process_chunks_to_vectors(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert chunks to vector format required by Pinecone."""
    vectors = []
    for i, chunk in enumerate(chunks):
        try:
            # Create a unique ID that includes source and position
            chunk_id = f"{chunk['source']}_{chunk['start_char']}_{chunk['end_char']}"
            
            # Get embedding for the chunk
            embedding = embed_text(chunk['text'])
            
            # Format vector according to Pinecone's API
            vector = {
                "id": chunk_id,
                "values": embedding,
                "metadata": {
                    'text': chunk['text'],
                    'source': chunk['source'],
                    'start_char': chunk['start_char'],
                    'end_char': chunk['end_char']
                }
            }
            vectors.append(vector)
            
            # Print progress
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(chunks)} chunks")
                
        except Exception as e:
            print(f"Error processing chunk {i}: {str(e)}")
            continue
            
    return vectors

def upsert_with_retry(vectors: List[Dict[str, Any]], retries: int = MAX_RETRIES) -> bool:
    """Upsert vectors with retry logic."""
    for attempt in range(retries):
        try:
            index.upsert(vectors=vectors)
            return True
        except Exception as e:
            if attempt == retries - 1:  # Last attempt
                print(f"Failed to upsert after {retries} attempts: {str(e)}")
                return False
            print(f"Upsert attempt {attempt + 1} failed, retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY * (attempt + 1))  # Exponential backoff
    return False

def process_and_upsert_chunks(chunks: List[Dict[str, Any]], batch_size: int = BATCH_SIZE):
    """Process chunks in batches and upsert to Pinecone with proper batching and retry logic."""
    total_chunks = len(chunks)
    print(f"Processing {total_chunks} chunks...")
    
    # Convert all chunks to vectors first
    vectors = process_chunks_to_vectors(chunks)
    
    # Process in batches
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        print(f"Upserting batch {i//batch_size + 1}/{(len(vectors) + batch_size - 1)//batch_size}")
        
        if upsert_with_retry(batch):
            print(f"Successfully upserted batch of {len(batch)} vectors. Progress: {min(i + batch_size, len(vectors))}/{len(vectors)}")
        else:
            print(f"Failed to upsert batch starting at index {i}")

def query_index(query_text: str, top_k: int = 5) -> Dict:
    """Query the index and return top matches."""
    query_embedding = embed_text(query_text)
    query_result = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    return query_result

if __name__ == "__main__":
    print("Testing connection to Pinecone index:", PINECONE_INDEX_NAME)
    print(f"Using environment: {PINECONE_ENVIRONMENT}")
    
    try:
        # Get initial index statistics
        index_stats = index.describe_index_stats()
        print(f"\nInitial Index Stats:")
        print(f"Total vectors: {index_stats.total_vector_count}")
        print(f"Dimension: {index_stats.dimension}\n")
        
        # Process all markdown files in the directory
        md_files = glob.glob(os.path.join(TEXTS_DIR, "*.md"))
        if not md_files:
            raise FileNotFoundError(f"No markdown files found in {TEXTS_DIR}")
            
        print(f"Found {len(md_files)} markdown files to process.")
        
        for file_path in md_files:
            filename = Path(file_path).name
            print(f"\nProcessing {filename}...")
            
            try:
                # Read and chunk the file
                text = read_markdown_file(file_path)
                chunks = chunk_text(text, filename)
                print(f"Created {len(chunks)} chunks from {filename}")
                
                # Process and upsert chunks
                process_and_upsert_chunks(chunks)
                
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")
                continue
        
        # Get final index statistics
        final_stats = index.describe_index_stats()
        print(f"\nFinal Index Stats:")
        print(f"Total vectors: {final_stats.total_vector_count}")
        
        # Try a test query
        test_query = "What does Wittgenstein say about language games?"
        print(f"\nRunning test query: '{test_query}'")
        
        results = query_index(test_query)
        
        print("\nQuery Results:")
        for match in results.matches:
            print(f"\nSource: {match.metadata['source']}")
            print(f"Score: {match.score:.4f}")
            print(f"Text: {match.metadata['text'][:200]}...")
            
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        raise 