"""
pdf_reader.py
Modular PDF text extraction engine powered by PyMuPDF (fitz).
Accepts PDF files only, displays file metadata, cleans extracted text,
and gracefully handles empty, corrupted, and scanned/image-only documents.
Zero external paid APIs. 100% local, secure, and private.
"""

import io
from typing import Dict, Any, Union, List, Optional
from nlp.text_cleaner import clean_text


def format_file_size(size_in_bytes: int) -> str:
    """Formats file size in bytes to a human-readable string (B, KB, MB)."""
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.1f} KB"
    else:
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"


def is_valid_pdf_stream(content: bytes) -> bool:
    """Verifies that the byte stream contains the standard PDF magic header."""
    if not content or len(content) < 5:
        return False
    # Standard PDF header is %PDF-1.x, can occasionally have leading comments/BOM
    return b"%PDF" in content[:1024]


def extract_text_from_pdf(file_source: Union[str, bytes, io.BytesIO], filename: str = "resume.pdf") -> Dict[str, Any]:
    """
    Extracts text and page metadata from a PDF file using PyMuPDF.

    Handles:
    - Empty PDF (0 bytes or blank pages)
    - Corrupted or truncated PDF
    - Scanned / image-only PDF (no selectable text)
    - Password-protected PDF
    - Extraction failures

    Returns structured dictionary with metadata, cleaned text, and diagnostics.
    """
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz

    # Initialize result structure
    result: Dict[str, Any] = {
        "success": False,
        "filename": filename,
        "text": "",
        "raw_text": "",
        "page_count": 0,
        "file_size": 0,
        "file_size_formatted": "0 B",
        "char_count": 0,
        "word_count": 0,
        "is_scanned": False,
        "is_empty": False,
        "is_encrypted": False,
        "error_type": None,
        "error": None,
        "page_texts": [],
    }

    doc = None
    try:
        raw_bytes = b""
        if isinstance(file_source, str):
            with open(file_source, "rb") as f:
                raw_bytes = f.read()
        elif isinstance(file_source, bytes):
            raw_bytes = file_source
        elif hasattr(file_source, "read"):
            raw_bytes = file_source.read()
            if hasattr(file_source, "seek"):
                file_source.seek(0)
        else:
            result["error_type"] = "invalid_source"
            result["error"] = "Unsupported file source format."
            return result

        result["file_size"] = len(raw_bytes)
        result["file_size_formatted"] = format_file_size(len(raw_bytes))

        # Check for empty file
        if len(raw_bytes) == 0:
            result["is_empty"] = True
            result["error_type"] = "empty"
            result["error"] = "The uploaded PDF file is empty (0 bytes)."
            return result

        # Validate PDF magic header
        if not is_valid_pdf_stream(raw_bytes):
            result["error_type"] = "corrupted"
            result["error"] = "Invalid PDF file. The document does not contain a valid PDF file header."
            return result

        # Open document with PyMuPDF
        try:
            doc = fitz.open(stream=raw_bytes, filetype="pdf")
        except Exception as open_err:
            result["error_type"] = "corrupted"
            result["error"] = f"Failed to open PDF document: {str(open_err)}. The file may be damaged or corrupted."
            return result

        # Check if password-protected
        if doc.is_encrypted:
            result["is_encrypted"] = True
            result["error_type"] = "encrypted"
            result["error"] = "The uploaded PDF is password-protected. Please provide an unlocked PDF document."
            return result

        page_count = len(doc)
        result["page_count"] = page_count

        if page_count == 0:
            result["is_empty"] = True
            result["error_type"] = "empty"
            result["error"] = "The uploaded PDF contains zero pages."
            return result

        # Iterate through pages and extract text
        page_texts: List[str] = []
        total_images = 0

        for page_idx in range(page_count):
            page = doc.load_page(page_idx)
            page_text = page.get_text("text") or ""
            page_texts.append(page_text.strip())

            # Count images for scanned document detection
            images = page.get_images()
            total_images += len(images)

        raw_combined = "\n\n".join(page_texts).strip()
        result["raw_text"] = raw_combined
        result["page_texts"] = page_texts

        # Clean extracted text
        cleaned_combined = clean_text(raw_combined)
        result["text"] = cleaned_combined
        result["char_count"] = len(cleaned_combined)
        result["word_count"] = len(cleaned_combined.split())

        # Check for scanned / image-only PDF
        # If very little selectable text (< 40 characters) but document has images or pages
        if len(cleaned_combined.strip()) < 40:
            if total_images > 0:
                result["is_scanned"] = True
                result["error_type"] = "scanned"
                result["error"] = (
                    "This PDF appears to be a scanned image without selectable text. "
                    "Please upload a text-based PDF exported directly from Word, Google Docs, LaTeX, or Canva."
                )
                return result
            else:
                result["is_empty"] = True
                result["error_type"] = "empty"
                result["error"] = "The uploaded PDF appears to be blank. No selectable text was found on any page."
                return result

        # Success!
        result["success"] = True
        return result

    except Exception as e:
        result["error_type"] = "extraction_failure"
        result["error"] = f"An unexpected error occurred during PDF text extraction: {str(e)}"
        return result

    finally:
        if doc is not None:
            try:
                doc.close()
            except Exception:
                pass


def extract_text_from_file(file_obj) -> Dict[str, Any]:
    """
    Streamlit-compatible file extractor that strictly enforces PDF uploads.
    Extracts, cleans, and validates resume documents.
    """
    filename = getattr(file_obj, "name", "resume.pdf")

    # Strict PDF-only validation as requested
    if not filename.lower().endswith(".pdf"):
        return {
            "success": False,
            "filename": filename,
            "text": "",
            "raw_text": "",
            "page_count": 0,
            "file_size": 0,
            "file_size_formatted": "0 B",
            "char_count": 0,
            "word_count": 0,
            "is_scanned": False,
            "is_empty": False,
            "is_encrypted": False,
            "error_type": "invalid_extension",
            "error": f"Invalid file format: '{filename}'. Please upload a PDF file only (.pdf).",
            "page_texts": [],
        }

    return extract_text_from_pdf(file_obj, filename=filename)
