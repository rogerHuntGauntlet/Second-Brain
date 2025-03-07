"""
Interactive CLI tool to upload .docx files to Pinecone
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog
import docx2txt
from dotenv import load_dotenv
from openai import OpenAI
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        logger.error(f"Error extracting text from {file_path}: {str(e)}")
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
    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        raise

def is_valid_vector(vector):
    """Check if a vector is valid for Pinecone (contains non-zero values)."""
    # Convert to numpy array for easier validation
    vec_array = np.array(vector)
    
    # Check if all values are zero
    if np.all(vec_array == 0):
        return False
    
    # Check if vector contains NaN or infinite values
    if np.any(np.isnan(vec_array)) or np.any(np.isinf(vec_array)):
        return False
    
    return True

def upload_to_pinecone(chunks, file_path, namespace, index, client):
    """Upload text chunks and their embeddings to Pinecone."""
    filename = os.path.basename(file_path)
    base_filename = os.path.splitext(filename)[0].replace(" ", "_").replace("-", "_")
    
    print(f"Uploading {len(chunks)} chunks to namespace: {namespace}")
    
    vectors = []
    valid_chunks = 0
    invalid_chunks = 0
    
    for i, chunk in enumerate(chunks):
        try:
            # Skip empty chunks
            if not chunk.strip():
                logger.warning(f"Skipping empty chunk {i}")
                invalid_chunks += 1
                continue
                
            vector = get_embedding(chunk, client)
            
            # Validate the vector
            if not is_valid_vector(vector):
                logger.warning(f"Skipping chunk {i} - invalid vector generated")
                invalid_chunks += 1
                continue
            
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
            
            valid_chunks += 1
            
            # Show progress
            if (i + 1) % 5 == 0 or i == len(chunks) - 1:
                print(f"Processed {i + 1}/{len(chunks)} chunks")
                
        except Exception as e:
            logger.error(f"Error processing chunk {i}: {str(e)}")
            invalid_chunks += 1
            continue
    
    # Upload vectors in batches to avoid request size limits
    batch_size = 100  # Pinecone recommends batches of 100 vectors
    
    if vectors:
        try:
            logger.info(f"Upserting {len(vectors)} vectors to namespace: {namespace}")
            
            # Process in batches
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i+batch_size]
                logger.info(f"Upserting batch {i//batch_size + 1}/{(len(vectors)-1)//batch_size + 1} with {len(batch)} vectors")
                
                # Perform the upsert operation
                upsert_response = index.upsert(vectors=batch, namespace=namespace)
                logger.info(f"Batch upsert response: {upsert_response}")
                print(f"Uploaded batch {i//batch_size + 1}/{(len(vectors)-1)//batch_size + 1} with {len(batch)} vectors")
            
            print(f"Successfully uploaded {valid_chunks} vectors to namespace: {namespace}")
            if invalid_chunks > 0:
                print(f"Skipped {invalid_chunks} invalid chunks")
                
        except Exception as e:
            logger.error(f"Error uploading to Pinecone: {str(e)}")
            print(f"Error uploading to Pinecone: {str(e)}")
            raise
    else:
        logger.warning("No valid vectors to upload")
        print("No valid vectors to upload. Please check your document content.")

def select_docx_file():
    """Open a file dialog to select a .docx file."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    file_path = filedialog.askopenfilename(
        title="Select a .docx file",
        filetypes=[("Word Documents", "*.docx")]
    )
    
    root.destroy()
    return file_path

def main():
    print("=" * 50)
    print("DOCX to Pinecone Uploader")
    print("=" * 50)
    
    # Get API keys from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_index = os.getenv("PINECONE_INDEX")
    pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
    
    # Validate required environment variables
    if not all([openai_api_key, pinecone_api_key, pinecone_index, pinecone_environment]):
        print("Error: Missing required environment variables.")
        print("Please set OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX, and PINECONE_ENVIRONMENT in your .env file.")
        sys.exit(1)
    
    # Get namespace from user
    namespace = input("Enter the Pinecone namespace: ")
    if not namespace:
        print("Error: Namespace cannot be empty.")
        sys.exit(1)
    
    # Get docx file path using file dialog
    print("Please select a .docx file...")
    docx_path = select_docx_file()
    
    if not docx_path:
        print("No file selected. Exiting.")
        sys.exit(0)
    
    # Validate file exists and is a docx
    if not os.path.exists(docx_path):
        print(f"Error: File not found: {docx_path}")
        sys.exit(1)
    
    if not docx_path.lower().endswith('.docx'):
        print(f"Error: File must be a .docx file: {docx_path}")
        sys.exit(1)
    
    # Initialize clients
    print("Initializing OpenAI and Pinecone clients...")
    openai_client = OpenAI(api_key=openai_api_key)
    
    try:
        # Initialize Pinecone with environment
        pc = pinecone.Pinecone(api_key=pinecone_api_key)
        logger.info(f"Pinecone initialized with API key: {pinecone_api_key[:5]}...")
        
        # Connect to the index
        index = pc.Index(name=pinecone_index)
        logger.info(f"Connected to Pinecone index: {pinecone_index}")
        
        # Test the connection
        stats = index.describe_index_stats()
        logger.info(f"Index stats: {stats}")
        print(f"Connected to Pinecone index: {pinecone_index}")
        print(f"Current index stats: {stats}")
    except Exception as e:
        logger.error(f"Error connecting to Pinecone: {str(e)}")
        print(f"Error connecting to Pinecone: {str(e)}")
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
    try:
        upload_to_pinecone(chunks, docx_path, namespace, index, openai_client)
        
        print("\n✅ Upload complete!")
        print(f"Document: {os.path.basename(docx_path)}")
        print(f"Namespace: {namespace}")
        print(f"Index: {pinecone_index}")
        print(f"Chunks processed: {len(chunks)}")
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        print(f"\n❌ Upload failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 