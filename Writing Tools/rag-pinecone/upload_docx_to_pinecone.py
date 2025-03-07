"""
Simple script to upload a docx file to Pinecone
"""

import os
import sys
import docx2txt
from dotenv import load_dotenv
from openai import OpenAI
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

# Constants
EMBEDDING_MODEL = "text-embedding-ada-002"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def extract_text_from_docx(file_path):
    """Extract text from a docx file."""
    try:
        text = docx2txt.process(file_path)
        return text
    except Exception as e:
        print(f"Error extracting text from {file_path}: {str(e)}")
        sys.exit(1)

def chunk_text(text):
    """Split text into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)

def get_embedding(text, client):
    """Generate embeddings using OpenAI's API."""
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding

def upload_to_pinecone(chunks, file_path, namespace, index, client):
    """Upload text chunks and their embeddings to Pinecone."""
    filename = os.path.basename(file_path)
    base_filename = os.path.splitext(filename)[0].replace(" ", "_").replace("-", "_")
    
    print(f"Uploading {len(chunks)} chunks to namespace: {namespace}")
    
    vectors = []
    for i, chunk in enumerate(chunks):
        vector = get_embedding(chunk, client)
        
        # Create a descriptive ID that includes filename and chunk number
        chunk_id = f"{base_filename}_chunk_{i:03d}"
        
        vectors.append({
            "id": chunk_id,
            "values": vector,
            "metadata": {
                "text": chunk,
                "source": file_path,
                "filename": filename
            }
        })
        
        # Show progress
        if (i + 1) % 5 == 0 or i == len(chunks) - 1:
            print(f"Processed {i + 1}/{len(chunks)} chunks")
    
    # Upload all vectors at once
    if vectors:
        index.upsert(vectors=vectors, namespace=namespace)
        print(f"Successfully uploaded {len(vectors)} vectors to namespace: {namespace}")

def main():
    # Get API keys from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_index = os.getenv("PINECONE_INDEX")
    
    # Validate required environment variables
    if not all([openai_api_key, pinecone_api_key, pinecone_index]):
        print("Error: Missing required environment variables.")
        print("Please set OPENAI_API_KEY, PINECONE_API_KEY, and PINECONE_INDEX in your .env file.")
        sys.exit(1)
    
    # Get docx file path
    if len(sys.argv) > 1:
        docx_path = sys.argv[1]
    else:
        docx_path = input("Enter the path to your docx file: ")
    
    # Validate file exists and is a docx
    if not os.path.exists(docx_path):
        print(f"Error: File not found: {docx_path}")
        sys.exit(1)
    
    if not docx_path.lower().endswith('.docx'):
        print(f"Error: File must be a .docx file: {docx_path}")
        sys.exit(1)
    
    # Get namespace
    if len(sys.argv) > 2:
        namespace = sys.argv[2]
    else:
        namespace = input("Enter the Pinecone namespace: ")
    
    # Initialize clients
    print("Initializing OpenAI and Pinecone clients...")
    openai_client = OpenAI(api_key=openai_api_key)
    pc = pinecone.Pinecone(api_key=pinecone_api_key)
    
    # Connect to the index
    try:
        index = pc.Index(name=pinecone_index)
        print(f"Connected to Pinecone index: {pinecone_index}")
    except Exception as e:
        print(f"Error connecting to Pinecone index: {str(e)}")
        sys.exit(1)
    
    # Process the docx file
    print(f"Processing {docx_path}...")
    text = extract_text_from_docx(docx_path)
    print(f"Extracted {len(text)} characters from document")
    
    # Chunk the text
    print("Splitting text into chunks...")
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")
    
    # Upload to Pinecone
    print("Uploading to Pinecone...")
    upload_to_pinecone(chunks, docx_path, namespace, index, openai_client)
    
    print("✅ Upload complete!")

if __name__ == "__main__":
    main() 