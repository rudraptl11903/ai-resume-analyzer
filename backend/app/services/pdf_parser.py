import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts all text from a given PDF file.
    """
    text = ""
    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)
        
        # Iterate through each page and extract text
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
            
        doc.close()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        
    return text

if __name__ == "__main__":
    # Example usage based on the prompt
    import sys
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = "Resume.pdf"
        
    print(f"Extracting text from: {pdf_path}")
    extracted_text = extract_text_from_pdf(pdf_path)
    print("--- Extracted Text ---")
    print(extracted_text)
