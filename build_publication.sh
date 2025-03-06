#!/bin/bash

echo "Publication Builder"
echo "================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed or not in PATH."
    echo "Please install Python 3.6+ and try again."
    exit 1
fi

# Check if config file exists
if [ ! -f publication_config.json ]; then
    echo "Warning: publication_config.json not found. Using default settings."
    python3 publication_builder.py
else
    python3 publication_builder.py --config publication_config.json
fi

echo
echo "Done! Combined manuscript is available at Witt-Trans/combined_manuscript.md" 