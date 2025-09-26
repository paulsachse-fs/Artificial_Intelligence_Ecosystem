#!/usr/bin/env python3
"""
PDF Extractor
-------------
Opens a PDF, extracts text from each page, cleans it, writes to
Selected_Document.txt (UTF-8), and returns the combined text.
"""

import re
from typing import Optional
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file and writes it to Selected_Document.txt.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Combined cleaned text from all pages.
    """
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print(f"❌ Failed to open PDF: {e}")
        return ""

    parts = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
            if text:
                # Collapse multiple whitespace characters
                text = re.sub(r"\s+", " ", text).strip()
                parts.append(text)
        except Exception as e:
            print(f"⚠️ Could not read page {i}: {e}")

    combined = "\n\n".join(parts)

    try:
        with open("Selected_Document.txt", "w", encoding="utf-8") as f:
            f.write(combined)
        print("✅ Wrote extracted text to Selected_Document.txt (UTF-8).")
    except OSError as e:
        print(f"❌ Failed to write output file: {e}")

    return combined


def main():
    pdf_path = "iPhone - Wikipedia.pdf"
    text = extract_text_from_pdf(pdf_path)
    if text:
        print("\n--- Preview (first 400 chars) ---")
        print(text[:400])
    else:
        print("\n⚠️ No text was extracted from the PDF.")


if __name__ == "__main__":
    main()
