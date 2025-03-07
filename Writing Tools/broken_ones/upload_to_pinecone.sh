#!/bin/bash

echo "==================================="
echo "Upload Writings to Pinecone Database"
echo "==================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        exit 1
    fi
fi

# Activate virtual environment
source .venv/bin/activate

# Install requirements if needed
if [ ! -d ".venv/lib/python*/site-packages/openai" ]; then
    echo "Installing requirements..."
    pip install -r requirements_pinecone.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install requirements."
        exit 1
    fi
fi

# Get directory from user if not provided
DIRECTORY=$1
if [ -z "$DIRECTORY" ]; then
    read -p "Enter directory path containing writings: " DIRECTORY
fi

# Get namespace from user if not provided
NAMESPACE=$2
if [ -z "$NAMESPACE" ]; then
    read -p "Enter Pinecone namespace (default: writings): " NAMESPACE
    if [ -z "$NAMESPACE" ]; then
        NAMESPACE="writings"
    fi
fi

# Get file pattern from user if not provided
PATTERN=$3
if [ -z "$PATTERN" ]; then
    read -p "Enter file pattern (default: **/*.md): " PATTERN
    if [ -z "$PATTERN" ]; then
        PATTERN="**/*.md"
    fi
fi

echo
echo "Running script with the following parameters:"
echo "Directory: $DIRECTORY"
echo "Namespace: $NAMESPACE"
echo "Pattern: $PATTERN"
echo

# Run the script
python upload_writings_to_pinecone.py --directory "$DIRECTORY" --namespace "$NAMESPACE" --pattern "$PATTERN"

# Deactivate virtual environment
deactivate

echo
echo "Script execution completed." 