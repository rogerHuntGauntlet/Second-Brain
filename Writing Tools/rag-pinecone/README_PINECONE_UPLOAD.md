# Upload Writings to Pinecone

This tool helps you upload your writings (markdown, text, or PDF files) to a Pinecone vector database for semantic search and retrieval.

## Features

- Process multiple file formats (Markdown, TXT, PDF)
- Automatically chunk text into manageable pieces
- Generate embeddings using OpenAI's embedding model
- Upload vectors to Pinecone with proper metadata
- Process entire directories recursively

## Prerequisites

1. An OpenAI API key
2. A Pinecone account and API key
3. Python 3.8 or higher

## Setup

1. Clone this repository or download the script files
2. Install the required dependencies:

```bash
pip install -r requirements_pinecone.txt
```

3. Create a `.env` file in the same directory as the script with the following variables:

```
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment  # e.g., us-east-1
PINECONE_INDEX=your_pinecone_index_name
```

## Usage

### Basic Usage

To upload all markdown files from a directory:

```bash
python upload_writings_to_pinecone.py --directory "path/to/your/writings" --namespace "my_writings"
```

### Advanced Options

```bash
python upload_writings_to_pinecone.py \
  --directory "path/to/your/writings" \
  --pattern "**/*.{md,txt}" \
  --namespace "my_writings" \
  --chunk-size 800 \
  --chunk-overlap 150
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--directory` | Directory containing writings to process | (Required) |
| `--pattern` | Glob pattern for files to process | `**/*.md` |
| `--namespace` | Pinecone namespace to use | `writings` |
| `--chunk-size` | Size of text chunks | 500 |
| `--chunk-overlap` | Overlap between chunks | 100 |

## How It Works

1. **Loading Documents**: The script loads documents from the specified directory matching the provided pattern.
2. **Chunking**: Each document is split into smaller chunks for better semantic representation.
3. **Embedding**: Each chunk is converted to a vector embedding using OpenAI's embedding model.
4. **Uploading**: The embeddings are uploaded to Pinecone with metadata including the original text and source information.

## Example Workflow

1. Organize your writings in a directory structure
2. Run the script to upload them to Pinecone
3. Use the Pinecone index for semantic search or retrieval-augmented generation (RAG)

## Troubleshooting

- **API Key Issues**: Ensure your API keys are correctly set in the `.env` file
- **Connection Errors**: Check your internet connection and Pinecone service status
- **File Format Errors**: Make sure your files are in the supported formats (MD, TXT, PDF)

## License

This project is open source and available under the MIT License. 