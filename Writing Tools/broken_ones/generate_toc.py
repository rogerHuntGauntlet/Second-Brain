from docx import Document
import re

def extract_headings(doc):
    """Extract headings from the document."""
    headings = []
    
    for paragraph in doc.paragraphs:
        if paragraph.style.name.startswith('Heading'):
            level = int(paragraph.style.name.split(' ')[1])
            if level <= 3:  # Only include headings 1-3
                headings.append((level, paragraph.text))
    
    return headings

def generate_toc_text(headings):
    """Generate text for table of contents."""
    toc_text = "TABLE OF CONTENTS\n\n"
    
    for level, text in headings:
        # Skip the "Table of Contents" heading itself
        if text.lower() == "table of contents":
            continue
            
        # Add indentation based on heading level
        indent = "    " * (level - 1)
        toc_text += f"{indent}{text}\n"
    
    return toc_text

def main():
    # Path to the document
    docx_path = r"C:\Users\roger\OneDrive\Desktop\Gauntlet_Projects\PROJECT-REVIEWS\()_SELF-ANALYSIS\AI Engineering Thesis\combined_thesis.docx"
    
    # Path for the TOC text file
    toc_path = r"C:\Users\roger\OneDrive\Desktop\Gauntlet_Projects\PROJECT-REVIEWS\()_SELF-ANALYSIS\AI Engineering Thesis\table_of_contents.txt"
    
    # Load the document
    doc = Document(docx_path)
    
    # Extract headings
    headings = extract_headings(doc)
    
    # Generate TOC text
    toc_text = generate_toc_text(headings)
    
    # Save TOC to a text file
    with open(toc_path, 'w', encoding='utf-8') as f:
        f.write(toc_text)
    
    print(f"Table of contents saved as {toc_path}")
    print("\nTable of Contents Preview:")
    print("==========================")
    print(toc_text)

if __name__ == "__main__":
    main() 