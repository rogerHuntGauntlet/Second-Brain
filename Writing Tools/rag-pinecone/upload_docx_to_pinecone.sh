#!/bin/bash

echo "==================================="
echo "DOCX to Pinecone Uploader"
echo "==================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH."
    echo "Please install Python from https://www.python.org/downloads/"
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "Error creating virtual environment."
        read -p "Press Enter to continue..."
        exit 1
    fi
fi

# Activate virtual environment
source .venv/bin/activate

# Install required packages if not already installed
echo "Checking required packages..."
pip install -r requirements_pinecone.txt

# Run the script
echo
echo "Starting uploader..."
echo
python3 docx_to_pinecone_cli.py

# Deactivate virtual environment
deactivate

echo
read -p "Press Enter to continue..." 