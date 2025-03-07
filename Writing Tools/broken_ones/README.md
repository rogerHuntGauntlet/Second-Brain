# Project Reviews and Analysis Collection

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)
[![Documentation](https://img.shields.io/badge/docs-up%20to%20date-green.svg)](README.md)

A comprehensive collection of in-depth technical analyses and reviews of popular technology platforms and services.

## Overview

This repository houses detailed project reviews and final presentation analyses of various technology platforms and services. Each analysis offers:

- Detailed technical insights
- Comprehensive evaluations
- Key learnings and best practices
- Architecture and implementation details

## Project Structure

```
SELF-ANALYSIS/
├── Circuit_FINAL_PRESENTATION.md
├── OSS_pull_request.md
├── Scribex_REVIEW_FINAL_PRESENTATION.md
├── Slack_REVIEW_FINAL_PRESENTATION.md
├── Tiktok_REVIEW_FINAL_PRESENTATION.md
└── Zendesk_REVIEW_FINAL_PRESENTATION.md
```

## Analyzed Projects

| Project | Description | Key Focus Areas |
|---------|-------------|----------------|
| Circuit | Feature-rich platform analysis | Architecture, Features, Implementation |
| OSS Contribution | Open source contribution insights | Best Practices, Pull Requests |
| Scribex | Platform review and analysis | UX, Technical Implementation |
| Slack | Communication platform deep-dive | Architecture, Integration, Features |
| TikTok | Social media platform analysis | Technical Stack, User Engagement |
| Zendesk | Customer service platform review | Features, Integration, Implementation |

## Purpose

This collection serves as a comprehensive knowledge base for:

- Technical analysis methodologies
- Architecture patterns and design decisions
- Implementation strategies and best practices
- Platform evaluation frameworks
- Comparative analysis techniques

## Usage Guide

Each analysis is documented in a dedicated markdown file following a consistent structure:

### Navigation
- Browse to the desired .md file
- Click to view the detailed analysis

### Content Structure
```
Analysis/
├── Platform Overview
├── Technical Architecture
├── Key Features
├── Implementation Details
└── Final Presentation Notes
```

## Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/analysis`)
3. Add your analysis following our template
4. Commit your changes (`git commit -am 'Add new analysis'`)
5. Push to the branch (`git push origin feature/analysis`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Made with love by the Project Analysis Team

Part of the Project Analysis Initiative

---

Note: This repository is part of a larger project analysis initiative. All analyses are based on publicly available information and personal research.

# Thesis Combiner

This script combines multiple markdown files from a thesis into a single publication-ready .docx document.

## Prerequisites

- Python 3.6 or higher
- Required Python packages (install using `pip install -r requirements.txt`):
  - python-docx
  - markdown
  - beautifulsoup4
  - lxml

## Usage

### Option 1: Using the Batch File (Windows)

Simply double-click the `run_thesis_combiner.bat` file. This will:
1. Check if Python is installed
2. Install required packages
3. Run the script
4. Display the results

### Option 2: Using PowerShell (Windows)

Right-click on `run_thesis_combiner.ps1` and select "Run with PowerShell". This will:
1. Check if Python is installed
2. Install required packages
3. Run the script with colorful output
4. Display the results

### Option 3: Manual Execution

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the script:
   ```
   python combine_thesis.py
   ```

## Publication-Ready Features

The script creates a professionally formatted document with:

- **Title Page**: Professional title page with thesis title, author name, and date
- **Table of Contents**: Automatically generated TOC with links to sections
- **Consistent Formatting**: Professional typography with Times New Roman font and proper spacing
- **Page Numbers**: Automatically added page numbers in footers
- **Section Organization**: Each markdown file becomes a properly formatted section
- **Academic Styling**: Double-spaced text with proper margins for publication

## Markdown Features Supported

The script supports the following markdown features:
- Headers (h1-h6) with proper hierarchical styling
- Paragraphs with formatting (bold, italic)
- Code blocks with syntax highlighting and proper monospace formatting
- Nested ordered and unordered lists
- Blockquotes with proper indentation
- Tables with header row styling
- Hyperlinks with proper formatting

## Customization

You can modify the input and output paths in the script:

```python
input_directory = r"C:\Users\roger\OneDrive\Desktop\Gauntlet_Projects\PROJECT-REVIEWS\()_SELF-ANALYSIS\AI Engineering Thesis\sections"
output_docx = r"C:\Users\roger\OneDrive\Desktop\Gauntlet_Projects\PROJECT-REVIEWS\()_SELF-ANALYSIS\AI Engineering Thesis\combined_thesis.docx"
```

You can also customize the title and author:

```python
convert_markdown_to_docx(
    input_directory, 
    output_docx,
    title="AI Engineering Thesis: A Framework for Building with AI",
    author="Roger Pincombe"
)
```

## Limitations

- Images in markdown are not currently supported
- Some complex nested markdown structures might require manual adjustment
- The table of contents will need to be updated in Word after opening (right-click and select "Update Field")

## Troubleshooting

If you encounter issues:

1. **Python not found**: Make sure Python is installed and added to your PATH
2. **Package installation errors**: Try running `pip install -r requirements.txt` manually
3. **File not found errors**: Verify the input directory path is correct
4. **Permission errors**: Make sure you have write access to the output directory
5. **TOC not showing**: After opening in Word, right-click the TOC and select "Update Field" 