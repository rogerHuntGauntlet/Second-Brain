import os
import re
import argparse
import json
from datetime import datetime

def extract_chapter_number(filename):
    """Extract chapter number from filename for proper sorting."""
    match = re.search(r'chapter(\d+)', filename)
    if match:
        return int(match.group(1))
    return float('inf')  # For non-standard named files, place them at the end

def generate_front_matter(config):
    """Generate front matter for the document based on the provided config."""
    front_matter = []
    
    # Title page
    front_matter.append(f"# {config.get('title', 'Complete Manuscript')}\n\n")
    
    # Author information
    if config.get('author'):
        front_matter.append(f"**Author:** {config.get('author')}\n\n")
    
    # Institution/affiliation
    if config.get('institution'):
        front_matter.append(f"**Institution:** {config.get('institution')}\n\n")
    
    # Date
    date_format = config.get('date_format', '%B %d, %Y')
    date_str = config.get('date', datetime.now().strftime(date_format))
    front_matter.append(f"**Date:** {date_str}\n\n")
    
    # Abstract
    if config.get('abstract'):
        front_matter.append("## Abstract\n\n")
        front_matter.append(f"{config.get('abstract')}\n\n")
    
    # Copyright notice
    if config.get('copyright'):
        front_matter.append(f"*{config.get('copyright')}*\n\n")
    
    front_matter.append("---\n\n")
    return "".join(front_matter)

def generate_toc(chapters, config):
    """Generate a table of contents from the chapter headings."""
    toc_lines = [f"# {config.get('toc_title', 'Table of Contents')}\n\n"]
    
    for idx, chapter in enumerate(chapters):
        # Get the first line which should be the chapter title
        with open(chapter, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        
        # Extract chapter title without the markdown heading syntax
        chapter_title = re.sub(r'^#+ ', '', first_line)
        
        # Add to TOC with proper link format
        toc_lines.append(f"{idx+1}. [{chapter_title}](#{chapter_title.lower().replace(' ', '-').replace(':', '').replace(',', '').replace('.', '').replace('(', '').replace(')', '')})\n")
    
    return "".join(toc_lines)

def process_chapter_content(content, chapter_index, config):
    """Process chapter content with additional formatting rules."""
    # Apply any chapter-specific transformations
    if config.get('add_chapter_prefix', True) and not content.strip().startswith('# Chapter'):
        # Add chapter prefix if it doesn't already exist
        if content.strip().startswith('# '):
            content = content.replace('# ', f'# Chapter {chapter_index}: ', 1)
    
    # Additional processing can be added here
    
    return content

def combine_chapters(input_dir, output_file, config=None):
    """Combine all chapter markdown files into a single document with configuration options."""
    if config is None:
        config = {}
    
    # Find all markdown files
    all_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    # Sort files by chapter number
    chapter_files = sorted(all_files, key=extract_chapter_number)
    
    # Full paths for the files
    chapter_paths = [os.path.join(input_dir, f) for f in chapter_files]
    
    combined_content = []
    
    # Add front matter
    combined_content.append(generate_front_matter(config))
    
    # Add table of contents if requested
    if config.get('include_toc', True):
        toc = generate_toc(chapter_paths, config)
        combined_content.append(toc)
        combined_content.append("\n\n---\n\n")
    
    # Combine all chapters
    for index, filepath in enumerate(chapter_paths):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Process chapter content
            content = process_chapter_content(content, index, config)
            
            # Ensure each chapter starts on a new page with proper spacing
            if combined_content:
                combined_content.append("\n\n")
            
            combined_content.append(content)
            
            # Add page break unless it's the last chapter
            if index < len(chapter_paths) - 1:
                combined_content.append("\n\n---\n\n")
    
    # Add bibliography if provided
    if config.get('bibliography'):
        combined_content.append("\n\n# Bibliography\n\n")
        combined_content.append(config.get('bibliography'))
    
    # Write the combined content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("".join(combined_content))
    
    print(f"Successfully combined {len(chapter_paths)} chapters into {output_file}")
    print(f"Combined chapters: {', '.join(chapter_files)}")
    
    # Return the path to the created file
    return output_file

def export_to_other_formats(markdown_file, formats, config):
    """Export the markdown file to other formats using pandoc if available."""
    try:
        import subprocess
        
        for output_format in formats:
            output_file = os.path.splitext(markdown_file)[0] + '.' + output_format
            
            # Prepare command based on format
            if output_format == 'pdf':
                cmd = ['pandoc', markdown_file, '-o', output_file, '--pdf-engine=xelatex']
            elif output_format == 'docx':
                cmd = ['pandoc', markdown_file, '-o', output_file]
            elif output_format == 'html':
                cmd = ['pandoc', markdown_file, '-o', output_file, '--standalone', '--metadata', f'title={config.get("title", "Complete Manuscript")}']
            else:
                cmd = ['pandoc', markdown_file, '-o', output_file]
                
            # Add any template if provided
            if config.get(f'{output_format}_template'):
                cmd.extend(['--template', config.get(f'{output_format}_template')])
                
            # Execute the command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Successfully exported to {output_file}")
            else:
                print(f"Failed to export to {output_format}:")
                print(result.stderr)
                
    except ImportError:
        print("Could not export to other formats. Make sure pandoc is installed and in your PATH.")
    except Exception as e:
        print(f"Error during export: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine markdown chapters into a publication-ready document')
    parser.add_argument('--input_dir', default='Witt-Trans/sec_final', 
                        help='Directory containing markdown chapter files')
    parser.add_argument('--output_file', default='Witt-Trans/combined_manuscript.md',
                        help='Output file path')
    parser.add_argument('--config', 
                        help='Path to a JSON config file with publication settings')
    parser.add_argument('--title', 
                        help='Document title')
    parser.add_argument('--author', 
                        help='Author name')
    parser.add_argument('--no_toc', action='store_true', 
                        help='Skip generating a table of contents')
    parser.add_argument('--export_formats', nargs='+', choices=['pdf', 'docx', 'html', 'epub'],
                        help='Export to additional formats (requires pandoc)')
    
    args = parser.parse_args()
    
    # Prepare configuration
    config = {}
    
    # Load config from file if provided
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
    
    # Override with command line arguments
    if args.title:
        config['title'] = args.title
    if args.author:
        config['author'] = args.author
    if args.no_toc:
        config['include_toc'] = False
    
    # Ensure output directory exists
    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Combine chapters
    markdown_file = combine_chapters(args.input_dir, args.output_file, config)
    
    # Export to other formats if requested
    if args.export_formats:
        export_to_other_formats(markdown_file, args.export_formats, config) 