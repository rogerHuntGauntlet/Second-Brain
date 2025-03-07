"""
Test script to verify Pinecone connection
"""

import os
import sys
from dotenv import load_dotenv
import pinecone
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    print("=" * 50)
    print("Pinecone Connection Test")
    print("=" * 50)
    
    # Get API keys from environment
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_index = os.getenv("PINECONE_INDEX")
    pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
    
    # Validate required environment variables
    if not all([pinecone_api_key, pinecone_index, pinecone_environment]):
        print("Error: Missing required environment variables.")
        print("Please set PINECONE_API_KEY, PINECONE_INDEX, and PINECONE_ENVIRONMENT in your .env file.")
        sys.exit(1)
    
    print(f"Pinecone API Key: {pinecone_api_key[:5]}...")
    print(f"Pinecone Index: {pinecone_index}")
    print(f"Pinecone Environment: {pinecone_environment}")
    
    try:
        # Initialize Pinecone
        print("\nInitializing Pinecone client...")
        pc = pinecone.Pinecone(api_key=pinecone_api_key)
        logger.info("Pinecone client initialized")
        
        # Connect to the index
        print("Connecting to index...")
        index = pc.Index(name=pinecone_index)
        logger.info(f"Connected to index: {pinecone_index}")
        
        # Get index stats
        print("Getting index stats...")
        stats = index.describe_index_stats()
        logger.info(f"Index stats: {stats}")
        print(f"\nIndex stats: {stats}")
        
        # Test a simple upsert with a single vector
        namespace = "test_connection"
        print(f"\nTesting upsert to namespace: {namespace}")
        
        # Create a test vector with random values (1536 dimensions for OpenAI embeddings)
        random_vector = [random.uniform(-1, 1) for _ in range(1536)]
        test_vector = {
            "id": "test_vector_001",
            "values": random_vector,
            "metadata": {
                "text": "This is a test vector",
                "source": "test_script"
            }
        }
        
        # Upsert the test vector
        response = index.upsert(vectors=[test_vector], namespace=namespace)
        logger.info(f"Upsert response: {response}")
        print(f"Upsert response: {response}")
        
        # Query the test vector
        print("\nTesting query...")
        query_response = index.query(
            namespace=namespace,
            vector=random_vector,
            top_k=1,
            include_metadata=True
        )
        logger.info(f"Query response: {query_response}")
        print(f"Query response: {query_response}")
        
        # Delete the test vector
        print("\nCleaning up test vector...")
        delete_response = index.delete(ids=["test_vector_001"], namespace=namespace)
        logger.info(f"Delete response: {delete_response}")
        print(f"Delete response: {delete_response}")
        
        print("\n✅ Pinecone connection test successful!")
        
    except Exception as e:
        logger.error(f"Error testing Pinecone connection: {str(e)}")
        print(f"\n❌ Error testing Pinecone connection: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 