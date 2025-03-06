import os
import re
import argparse
from datetime import datetime

def extract_chapter_number(filename):
    """Extract chapter number from filename for proper sorting."""
    match = re.search(r'chapter(\d+)', filename)
    if match:
        return int(match.group(1))
    return -1  # For non-standard named files, place them at the beginning

def generate_toc(chapters):
    """Generate a table of contents from the chapter headings."""
    toc_lines = ["# Table of Contents\n\n"]
    
    for idx, chapter in enumerate(chapters):
        # Get the first line which should be the chapter title
        with open(chapter, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        
        # Extract chapter title without the markdown heading syntax
        chapter_title = re.sub(r'^#+ ', '', first_line)
        
        # Add to TOC with proper link format
        toc_lines.append(f"{idx+1}. [{chapter_title}](#{chapter_title.lower().replace(' ', '-')})\n")
    
    return "".join(toc_lines)

def combine_chapters(input_dir, output_file, include_toc=True):
    """Combine all chapter markdown files into a single document."""
    # Find all markdown files
    all_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    # Sort files by chapter number
    chapter_files = sorted(all_files, key=extract_chapter_number)
    
    # Full paths for the files
    chapter_paths = [os.path.join(input_dir, f) for f in chapter_files]
    
    # Start with a title page
    combined_content = [
        "# Complete Manuscript\n\n",
        f"*Combined on {datetime.now().strftime('%B %d, %Y')}*\n\n",
        "---\n\n"
    ]
    
    # Add table of contents if requested
    if include_toc:
        toc = generate_toc(chapter_paths)
        combined_content.append(toc)
        combined_content.append("\n\n---\n\n")
    
    # Combine all chapters
    for filepath in chapter_paths:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Ensure each chapter starts on a new page with proper spacing
            if combined_content:
                combined_content.append("\n\n")
            
            combined_content.append(content)
            combined_content.append("\n\n---\n\n")
    
    # Write the combined content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("".join(combined_content))
    
    print(f"Successfully combined {len(chapter_paths)} chapters into {output_file}")
    print(f"Combined chapters: {', '.join(chapter_files)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine markdown chapters into a single document')
    parser.add_argument('--input_dir', default='Witt-Trans/sec_final', 
                        help='Directory containing markdown chapter files')
    parser.add_argument('--output_file', default='Witt-Trans/combined_manuscript.md',
                        help='Output file path')
    parser.add_argument('--no_toc', action='store_true', 
                        help='Skip generating a table of contents')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    combine_chapters(args.input_dir, args.output_file, not args.no_toc) 