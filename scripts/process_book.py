#!/usr/bin/env python3
"""
Split a PDF into per-page text files arranged in X-page sections.

Output structure (created in the same directory as this script):
  {pdf_stem}/
    section_1/
      1.txt
      2.txt
      ...
      5.txt
    section_2/
      6.txt
      ...
    section_N/
      {last_page}.txt

Usage:
  python split_pdf_to_sections.py /path/to/file.pdf
"""

import argparse
import os
import re
import sys
import shutil
import json
from pathlib import Path
from pypdf import PdfReader

PAGES_PER_SECTION = 5


def create_index(text_path: Path):
    for section in os.listdir(text_path):
        section_path = text_path / section
        
        # Ensure it's a directory
        if os.path.isdir(section_path):
            # Get all .txt files in the section folder
            txt_files = [f for f in os.listdir(section_path) if f.endswith('.txt')]
            
            # Sort the files numerically based on the number in the filename
            txt_files.sort(key=lambda x: int(x.split('.')[0]))
            
            # Create the index.json file
            index_file_path = section_path / 'index.json'
            with open(index_file_path, 'w') as index_file:
                json.dump(txt_files, index_file)


def sanitize_text(text: str) -> str:
    """
    Normalize whitespace while preserving all characters (no word filtering).
    This keeps 'all the words' but avoids odd spacing from PDF extraction.
    """
    if text is None:
        return ""
    # Collapse consecutive whitespace to single spaces, keep newlines between paragraphs.
    # First normalize Windows newlines, then collapse runs of spaces/tabs.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Preserve double newlines (paragraphs), but normalize space runs within lines
    lines = [re.sub(r"[ \t\u00A0]+", " ", line).strip() for line in text.split("\n")]
    # Rebuild with '\n' so paragraphs remain readable
    return "\n".join(lines).strip()


def main():
    parser = argparse.ArgumentParser(description=f"Parse a PDF and write per-page text files grouped into {PAGES_PER_SECTION}-page sections.")
    parser.add_argument("pdf_path", type=Path, help="Path to the input PDF")
    args = parser.parse_args()

    pdf_path: Path = args.pdf_path
    if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
        print(f"Error: '{pdf_path}' does not exist or is not a PDF.", file=sys.stderr)
        sys.exit(1)

    # Create output directory structure
    base_path = pdf_path.parent / pdf_path.stem 
    text_path = base_path / f"{pdf_path.stem}_text"

    text_path.mkdir(parents=True, exist_ok=True)

    shutil.copy(pdf_path, base_path)

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as e:
        print(f"Failed to open PDF: {e}", file=sys.stderr)
        sys.exit(1)

    if reader.is_encrypted:
        try:
            # Try decrypting with empty password; many PDFs are "protected" but readable
            reader.decrypt("")
        except Exception:
            print("Error: PDF is encrypted and could not be opened without a password.", file=sys.stderr)
            sys.exit(1)

    num_pages = len(reader.pages)
    if num_pages == 0:
        print("PDF has 0 pages; nothing to do.", file=sys.stderr)
        sys.exit(1)

    for page_idx in range(num_pages):
        page_number = page_idx + 1  # 1-based
        section_number = (page_number - 1) // PAGES_PER_SECTION + 1
        section_dir = text_path / f"section_{section_number}"
        section_dir.mkdir(parents=True, exist_ok=True)

        try:
            text = reader.pages[page_idx].extract_text()
        except Exception as e:
            print(f"Warning: failed to extract text from page {page_number}: {e}", file=sys.stderr)
            text = ""

        cleaned = sanitize_text(text)
        # Write to {page_number}.txt inside its section
        out_file = section_dir / f"{page_number}.txt"
        try:
            out_file.write_text(cleaned, encoding="utf-8")
        except Exception as e:
            print(f"Error writing {out_file}: {e}", file=sys.stderr)
            sys.exit(1)

    print(f"Wrote {num_pages} pages into '{text_path}'.")
    print(f"Sections contain exactly {PAGES_PER_SECTION} pages each, except the last one which may have ≤{PAGES_PER_SECTION}.")
    print("Now creating index.json files for each section...")

    create_index(text_path)

    print("Removing pdf from source location now that processing is complete...")
    os.remove(pdf_path)


if __name__ == "__main__":
    main()
