# DOCX to Pinecone Uploader

A simple tool to upload content from Word (.docx) documents to your Pinecone vector database.

## Features

- Interactive command-line interface
- File selection dialog for choosing .docx files
- Namespace selection for organizing your vectors
- Automatic text chunking and embedding generation
- Progress tracking during upload

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Pinecone API key and index

## Setup

1. Ensure you have a `.env` file in the root directory with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX=your_pinecone_index_name
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements_pinecone.txt
   ```

## Usage

### Windows

1. Double-click the `upload_docx_to_pinecone.bat` file
2. Enter the namespace when prompted
3. Select a .docx file using the file dialog
4. Wait for the upload to complete

### macOS/Linux

1. Make the script executable:
   ```
   chmod +x upload_docx_to_pinecone.sh
   ```

2. Run the script:
   ```
   ./upload_docx_to_pinecone.sh
   ```

3. Enter the namespace when prompted
4. Select a .docx file using the file dialog
5. Wait for the upload to complete

## How It Works

1. The script extracts text from the selected .docx file
2. The text is split into smaller chunks (default: 500 characters with 100 character overlap)
3. Each chunk is converted to an embedding using OpenAI's embedding model
4. The embeddings and original text are uploaded to your Pinecone index under the specified namespace

## Configuration

You can modify the following constants in the `docx_to_pinecone_cli.py` file:

- `EMBEDDING_MODEL`: The OpenAI embedding model to use (default: "text-embedding-ada-002")
- `CHUNK_SIZE`: The size of each text chunk in characters (default: 500)
- `CHUNK_OVERLAP`: The overlap between chunks in characters (default: 100)

## Troubleshooting

- **Missing API keys**: Ensure your `.env` file is properly configured with valid API keys
- **File selection issues**: Make sure you have a graphical environment available for the file dialog
- **Package installation errors**: Try manually installing the required packages:
  ```
  pip install openai pinecone-client langchain python-dotenv docx2txt tkinter
  ```

## License

This project is open source and available under the MIT License. 