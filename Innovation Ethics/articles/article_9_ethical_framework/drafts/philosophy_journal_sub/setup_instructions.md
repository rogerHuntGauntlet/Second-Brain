# Document Formatting Setup Instructions

## Required Software

1. **Pandoc** (Document Converter)
   - Windows: `choco install pandoc`
   - Or download from: https://pandoc.org/installing.html

2. **LaTeX** (for PDF output)
   - Windows: `choco install miktex`
   - Or download from: https://miktex.org/download

3. **Citation Style**
   - Download Philosophy & Technology CSL style from:
   - https://www.zotero.org/styles/philosophy-and-technology
   - Save as `philosophy-and-technology.csl` in the same directory

## Converting the Document

### To PDF
```bash
pandoc synthesis_paper.md -o paper.pdf --pdf-engine=xelatex --filter=pandoc-citeproc --metadata-file=metadata.yaml --bibliography=references.bib --csl=philosophy-and-technology.csl
```

### To DOCX (Microsoft Word)
```bash
pandoc synthesis_paper.md -o paper.docx --filter=pandoc-citeproc --metadata-file=metadata.yaml --bibliography=references.bib --csl=philosophy-and-technology.csl --reference-doc=template.docx
```

## File Structure
- `synthesis_paper.md`: Main manuscript
- `metadata.yaml`: Document metadata and formatting
- `references.bib`: Bibliography in BibTeX format
- `philosophy-and-technology.csl`: Citation style
- `template.docx` (optional): Word template for formatting

## Notes
- The PDF output will be properly formatted according to academic standards
- Citations will be automatically formatted according to the journal style
- The YAML metadata ensures consistent formatting
- Double-spacing and proper margins are automatically applied 