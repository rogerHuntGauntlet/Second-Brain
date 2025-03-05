import os
import openai
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
import pdfplumber
from dotenv import load_dotenv
import glob
from openai import OpenAI

# Load environment variables
load_dotenv()

# Set API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")
PINECONE_INDEX = "phd-knowledge"
PINECONE_NAMESPACE = "witt_works"

print(f"Using Pinecone index: {PINECONE_INDEX}")
print(f"Using Pinecone namespace: {PINECONE_NAMESPACE}")

# Initialize OpenAI & Pinecone
client = OpenAI(api_key=OPENAI_API_KEY)
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Connect to the index
try:
    index = pc.Index(name=PINECONE_INDEX)
    # Test the connection
    stats = index.describe_index_stats()
    print("Successfully connected to Pinecone index!")
    print(f"Current index stats: {stats}")
except Exception as e:
    print(f"Error connecting to Pinecone index: {str(e)}")
    exit(1)

def load_pdf(file_path):
    """Read text from a PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def load_markdown(file_path):
    """Read text from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def load_document(file_path):
    """Load document based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return load_pdf(file_path)
    elif ext in ['.md', '.txt']:
        return load_markdown(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def chunk_text(text, chunk_size=500, chunk_overlap=100):
    """Split text into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)

def get_embedding(text):
    """Generate embeddings using OpenAI's API."""
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

def upload_to_pinecone(chunks, metadata=None):
    """Upload text chunks and their embeddings to Pinecone."""
    filename = metadata.get("filename", "doc") if metadata else "doc"
    # Remove file extension and replace spaces/special chars with underscores
    base_filename = os.path.splitext(filename)[0].replace(" ", "_").replace("-", "_")
    
    vectors = []
    for i, chunk in enumerate(chunks):
        vector = get_embedding(chunk)
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
        
        # Upload in batches of 100 to avoid timeouts
        if len(vectors) >= 100:
            index.upsert(vectors=vectors, namespace=PINECONE_NAMESPACE)
            print(f"Uploaded batch of {len(vectors)} vectors to {PINECONE_NAMESPACE} namespace")
            vectors = []
    
    # Upload any remaining vectors
    if vectors:
        index.upsert(vectors=vectors, namespace=PINECONE_NAMESPACE)
        print(f"Uploaded final batch of {len(vectors)} vectors to {PINECONE_NAMESPACE} namespace")

def process_and_upload(file_path, metadata=None):
    """Main function to process document and upload to Pinecone."""
    print(f"🔹 Processing {file_path}...")
    try:
        text = load_document(file_path)
        
        print("🔹 Splitting into chunks...")
        chunks = chunk_text(text)
        
        if metadata is None:
            metadata = {
                "source": file_path,
                "filename": os.path.basename(file_path)
            }
        
        print("🔹 Uploading to Pinecone...")
        upload_to_pinecone(chunks, metadata)
        print("✅ Upload complete!")
        return True
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
        return False

def process_directory(directory_path, file_pattern="**/*.md"):
    """Process all matching files in a directory recursively."""
    files = glob.glob(os.path.join(directory_path, file_pattern), recursive=True)
    print(f"Found {len(files)} files to process")
    
    successful = 0
    for file_path in files:
        if process_and_upload(file_path):
            successful += 1
            
    print(f"\n✨ Processing complete! Successfully processed {successful}/{len(files)} files")

if __name__ == "__main__":
    # Process only chapter 8 directory
    process_directory("Witt-Trans/sections/ch8", "**/*.md") 