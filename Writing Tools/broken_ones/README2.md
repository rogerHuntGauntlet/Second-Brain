# Publication Builder for Markdown Chapters

This project provides scripts to combine multiple markdown chapter files into a single, publication-ready document. It includes two scripts with varying levels of functionality:

1. `combine_chapters.py`: A simple script for basic chapter combination
2. `publication_builder.py`: An enhanced script with additional features like custom title, author information, and export capabilities

## Requirements

- Python 3.6+
- For export capabilities: Pandoc (optional)

## Basic Usage

### Simple Combination

```bash
python combine_chapters.py
```

This will combine all markdown files in the `Witt-Trans/sec_final` directory into a single file named `Witt-Trans/combined_manuscript.md`.

You can customize the input and output paths:

```bash
python combine_chapters.py --input_dir "path/to/chapters" --output_file "path/to/output.md"
```

Additional options:
- `--no_toc`: Skip generating a table of contents

### Enhanced Publication Builder

For more control over the output, use the enhanced publication builder:

```bash
python publication_builder.py --config publication_config.json
```

The configuration file allows you to specify:
- Document title and author information
- Abstract and copyright notice
- Bibliography entries
- TOC settings
- Chapter prefix behaviors

You can also specify individual options via command line:

```bash
python publication_builder.py --title "My Book Title" --author "My Name" --export_formats pdf docx
```

## Export to Other Formats

The enhanced script can export to other formats if you have Pandoc installed:

```bash
python publication_builder.py --config publication_config.json --export_formats pdf docx html
```

Supported formats:
- PDF
- DOCX (Word)
- HTML
- EPUB

## Configuration

Edit the `publication_config.json` file to customize your publication details:

```json
{
  "title": "Your Book Title",
  "author": "Your Name",
  "institution": "Your Institution",
  "abstract": "A brief summary of your work",
  "copyright": "© 2023 All Rights Reserved",
  "bibliography": "Your bibliography entries"
}
```

## How It Works

The scripts:
1. Find all markdown files in the specified directory
2. Sort them based on chapter numbers in filenames
3. Generate a table of contents from chapter headings
4. Combine chapters with proper formatting and spacing
5. Add front matter and bibliography if requested
6. Export to other formats if requested and Pandoc is available

## Customizing Chapter Processing

You can modify the `process_chapter_content` function in `publication_builder.py` to implement custom formatting rules for your chapters.

## Troubleshooting

- **File Not Found**: Make sure the input directory path is correct and contains markdown files
- **Export Failures**: Ensure Pandoc is installed and in your PATH if using export features
- **Encoding Issues**: The scripts use UTF-8 encoding; ensure your source files are compatible 