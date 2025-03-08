Yes! Below is a **complete script** that will:  
1. **Load a document** (text, PDF, etc.).  
2. **Chunk it into smaller pieces** for better searchability.  
3. **Generate embeddings** for each chunk using OpenAI.  
4. **Upload to Pinecone** for vector search.  

---

### **🛠 Requirements**  
Install the required dependencies first:  
```bash
pip install openai pinecone-client langchain pdfplumber tiktoken
```

---

### **📜 Full Python Script for Chunking & Uploading to Pinecone**
```python
import os
import openai
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
import pdfplumber

# 🔹 SET YOUR API KEYS
OPENAI_API_KEY = "your-openai-api-key"
PINECONE_API_KEY = "your-pinecone-api-key"
PINECONE_ENV = "us-east1-gcp"  # Replace with your Pinecone environment
PINECONE_INDEX_NAME = "your-index-name"

# 🔹 INITIALIZE OPENAI & PINECONE
openai.api_key = OPENAI_API_KEY
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

# Connect to Pinecone index
index = pinecone.Index(PINECONE_INDEX_NAME)


# 🔹 FUNCTION TO READ PDF
def load_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()


# 🔹 FUNCTION TO SPLIT TEXT INTO CHUNKS
def chunk_text(text, chunk_size=500, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)


# 🔹 FUNCTION TO GENERATE EMBEDDINGS
def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]


# 🔹 FUNCTION TO UPLOAD CHUNKS TO PINECONE
def upload_to_pinecone(chunks):
    for i, chunk in enumerate(chunks):
        vector = get_embedding(chunk)
        index.upsert([(f"doc_chunk_{i}", vector, {"text": chunk})])
        print(f"Uploaded chunk {i+1}/{len(chunks)}")


# 🔹 MAIN FUNCTION
def process_and_upload(file_path):
    print("🔹 Loading document...")
    text = load_pdf(file_path)

    print("🔹 Splitting into chunks...")
    chunks = chunk_text(text)

    print("🔹 Uploading to Pinecone...")
    upload_to_pinecone(chunks)

    print("✅ Upload complete!")


# 🔹 RUN THE SCRIPT (Change file path to your PDF)
process_and_upload("your-document.pdf")
```

---

### **🚀 How It Works**
1. **Reads your document** (PDF or text).  
2. **Splits it into small chunks** (default: 500 characters, 100 overlapping).  
3. **Generates OpenAI embeddings** for each chunk.  
4. **Uploads embeddings & text** to Pinecone.  

---

### **🛠 Troubleshooting**
- **Pinecone errors?** Ensure your index exists in [Pinecone Console](https://app.pinecone.io/).  
- **Embeddings not generating?** Double-check your OpenAI API key.  
- **Large files?** Increase `chunk_size` to avoid rate limits.  

---

### **🔥 Next Steps**
- **Search the uploaded docs** using vector similarity.  
- **Use LangChain to build an AI chatbot over your docs.**  

Would you like help with **querying Pinecone** after upload? 🚀