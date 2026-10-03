"""
pdf_reader.py
Fast, accurate text extraction using PyMuPDF (fitz) with docx and txt fallback.
Zero external cloud APIs required.
"""

import io
from typing import Dict, Any, Union


def extract_text_from_pdf(file_source: Union[str, bytes, io.BytesIO]) -> Dict[str, Any]:
    """
    Extracts plain text and page metadata from a PDF file using PyMuPDF (fitz).
    Accepts a filepath, raw bytes, or a Streamlit UploadedFile (BytesIO).
    """
    import fitz  # PyMuPDF

    doc = None
    try:
        if isinstance(file_source, str):
            doc = fitz.open(file_source)
        elif isinstance(file_source, bytes):
            doc = fitz.open(stream=file_source, filetype="pdf")
        elif hasattr(file_source, "read"):
            # Streamlit UploadedFile or BytesIO
            content = file_source.read()
            if hasattr(file_source, "seek"):
                file_source.seek(0)
            doc = fitz.open(stream=content, filetype="pdf")
        else:
            raise ValueError("Unsupported file source format")

        page_count = len(doc)
        full_text = []

        for page_idx in range(page_count):
            page = doc.load_page(page_idx)
            text = page.get_text("text")
            if text:
                full_text.append(text)

        extracted_text = "\n".join(full_text).strip()

        return {
            "success": True,
            "text": extracted_text,
            "page_count": page_count,
            "char_count": len(extracted_text),
            "word_count": len(extracted_text.split()),
            "error": None,
        }

    except Exception as e:
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "char_count": 0,
            "word_count": 0,
            "error": str(e),
        }
    finally:
        if doc is not None:
            doc.close()


def extract_text_from_file(file_obj) -> Dict[str, Any]:
    """
    Generic file extractor handling PDF, DOCX, and TXT files.
    Ideal for Streamlit file uploader inputs.
    """
    filename = getattr(file_obj, "name", "document.pdf").lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_obj)

    elif filename.endswith(".docx"):
        try:
            import docx
            doc = docx.Document(file_obj)
            text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            return {
                "success": True,
                "text": text,
                "page_count": 1,
                "char_count": len(text),
                "word_count": len(text.split()),
                "error": None,
            }
        except Exception as e:
            return {"success": False, "text": "", "page_count": 0, "error": str(e)}

    elif filename.endswith(".txt"):
        try:
            content = file_obj.read()
            if isinstance(content, bytes):
                text = content.decode("utf-8", errors="ignore")
            else:
                text = str(content)
            return {
                "success": True,
                "text": text,
                "page_count": 1,
                "char_count": len(text),
                "word_count": len(text.split()),
                "error": None,
            }
        except Exception as e:
            return {"success": False, "text": "", "page_count": 0, "error": str(e)}

    else:
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "error": f"Unsupported file format for {filename}. Please upload a PDF, DOCX, or TXT file."
        }
