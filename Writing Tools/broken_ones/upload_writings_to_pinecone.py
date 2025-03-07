"""
Upload Writings to Pinecone Vector Database

This script processes text files (markdown, txt, pdf) and uploads their embeddings to Pinecone.
It handles chunking, embedding generation, and vector database operations.

Usage:
    python upload_writings_to_pinecone.py --directory "path/to/writings" --pattern "**/*.md" --namespace "my_writings"

Requirements:
    - OpenAI API key
    - Pinecone API key and environment
    - Python packages: openai, pinecone-client, tiktoken, pdfplumber, python-dotenv
"""

import os
import argparse
import glob
from typing import Dict, List, Optional, Any, Union
import tiktoken
import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

# Constants
DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 100
DEFAULT_BATCH_SIZE = 100
EMBEDDING_MODEL = "text-embedding-ada-002"

class PineconeUploader:
    """Class to handle uploading text embeddings to Pinecone."""
    
    def __init__(
        self, 
        openai_api_key: str, 
        pinecone_api_key: str,
        pinecone_environment: str,
        pinecone_index: str,
        namespace: str = "default",
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
    ):
        """Initialize the uploader with API keys and configuration."""
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.pinecone_client = pinecone.Pinecone(api_key=pinecone_api_key)
        self.pinecone_index = self.pinecone_client.Index(name=pinecone_index)
        self.namespace = namespace
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        print(f"Initialized PineconeUploader with:")
        print(f"  - Index: {pinecone_index}")
        print(f"  - Namespace: {namespace}")
        print(f"  - Chunk size: {chunk_size}")
        print(f"  - Chunk overlap: {chunk_overlap}")
        
        # Test connection to Pinecone
        try:
            stats = self.pinecone_index.describe_index_stats()
            print(f"Successfully connected to Pinecone index!")
            print(f"Current index stats: {stats}")
        except Exception as e:
            print(f"Error connecting to Pinecone index: {str(e)}")
            raise
    
    def load_document(self, file_path: str) -> str:
        """Load document content based on file extension."""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return self._load_pdf(file_path)
        elif ext in ['.md', '.txt']:
            return self._load_text_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def _load_pdf(self, file_path: str) -> str:
        """Read text from a PDF file."""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    
    def _load_text_file(self, file_path: str) -> str:
        """Read text from a text-based file (markdown, txt)."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into smaller chunks for processing."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        return text_splitter.split_text(text)
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embeddings using OpenAI's API."""
        response = self.openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    
    def upload_to_pinecone(self, chunks: List[str], metadata: Optional[Dict[str, Any]] = None) -> None:
        """Upload text chunks and their embeddings to Pinecone."""
        filename = metadata.get("filename", "doc") if metadata else "doc"
        # Remove file extension and replace spaces/special chars with underscores
        base_filename = os.path.splitext(filename)[0].replace(" ", "_").replace("-", "_")
        
        vectors = []
        for i, chunk in enumerate(chunks):
            vector = self.get_embedding(chunk)
            chunk_metadata = {"text": chunk}
            if metadata:
                chunk_metadata.update(metadata)
            
            # Create a descriptive ID that includes filename and chunk number
            chunk_id = f"{base_filename}_chunk_{i:03d}"  # Use zero-padding for better sorting
            
            vectors.append({
                "id": chunk_id,
                "values": vector,
                "metadata": chunk_metadata
            })
            
            # Upload in batches to avoid timeouts
            if len(vectors) >= DEFAULT_BATCH_SIZE:
                self.pinecone_index.upsert(vectors=vectors, namespace=self.namespace)
                print(f"Uploaded batch of {len(vectors)} vectors to {self.namespace} namespace")
                vectors = []
        
        # Upload any remaining vectors
        if vectors:
            self.pinecone_index.upsert(vectors=vectors, namespace=self.namespace)
            print(f"Uploaded final batch of {len(vectors)} vectors to {self.namespace} namespace")
    
    def process_and_upload(self, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Process a single document and upload to Pinecone."""
        print(f"🔹 Processing {file_path}...")
        try:
            text = self.load_document(file_path)
            
            print("🔹 Splitting into chunks...")
            chunks = self.chunk_text(text)
            
            if metadata is None:
                metadata = {
                    "source": file_path,
                    "filename": os.path.basename(file_path)
                }
            
            print("🔹 Uploading to Pinecone...")
            self.upload_to_pinecone(chunks, metadata)
            print("✅ Upload complete!")
            return True
        except Exception as e:
            print(f"❌ Error processing {file_path}: {str(e)}")
            return False
    
    def process_directory(self, directory_path: str, file_pattern: str = "**/*.md") -> None:
        """Process all matching files in a directory recursively."""
        files = glob.glob(os.path.join(directory_path, file_pattern), recursive=True)
        print(f"Found {len(files)} files to process")
        
        successful = 0
        for file_path in files:
            if self.process_and_upload(file_path):
                successful += 1
                
        print(f"\n✨ Processing complete! Successfully processed {successful}/{len(files)} files")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Upload writings to Pinecone vector database")
    parser.add_argument("--directory", type=str, required=True, help="Directory containing writings to process")
    parser.add_argument("--pattern", type=str, default="**/*.md", help="Glob pattern for files to process (default: **/*.md)")
    parser.add_argument("--namespace", type=str, default="writings", help="Pinecone namespace to use (default: writings)")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE, help=f"Size of text chunks (default: {DEFAULT_CHUNK_SIZE})")
    parser.add_argument("--chunk-overlap", type=int, default=DEFAULT_CHUNK_OVERLAP, help=f"Overlap between chunks (default: {DEFAULT_CHUNK_OVERLAP})")
    
    args = parser.parse_args()
    
    # Get API keys from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
    pinecone_index = os.getenv("PINECONE_INDEX")
    
    # Validate required environment variables
    if not all([openai_api_key, pinecone_api_key, pinecone_environment, pinecone_index]):
        missing = []
        if not openai_api_key: missing.append("OPENAI_API_KEY")
        if not pinecone_api_key: missing.append("PINECONE_API_KEY")
        if not pinecone_environment: missing.append("PINECONE_ENVIRONMENT")
        if not pinecone_index: missing.append("PINECONE_INDEX")
        
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        print("Please set these variables in your .env file or environment.")
        return
    
    # Initialize uploader
    uploader = PineconeUploader(
        openai_api_key=openai_api_key,
        pinecone_api_key=pinecone_api_key,
        pinecone_environment=pinecone_environment,
        pinecone_index=pinecone_index,
        namespace=args.namespace,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap
    )
    
    # Process directory
    uploader.process_directory(args.directory, args.pattern)


if __name__ == "__main__":
    main() 