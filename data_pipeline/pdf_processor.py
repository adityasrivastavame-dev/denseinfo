import os
import pdfplumber

def extract_text_and_coordinates(pdf_path):
    """
    Reads an Italian hospital PDF and extracts all text with bounding boxes.
    This data will be sent to the AMD-powered LLM for synthesis.
    """
    results = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            words = page.extract_words()
            
            for word in words:
                results.append({
                    "text": word["text"],
                    "page": page_num + 1,
                    "bbox": {
                        "x0": word["x0"],         # Left edge
                        "top": word["top"],       # Top edge
                        "x1": word["x1"],         # Right edge
                        "bottom": word["bottom"]  # Bottom edge
                    }
                })
                
    return results

def get_raw_text_for_amd(pdf_path):
    """
    A helper function that just grabs the plain text.
    Aditya will send this text to the AMD ROCm vLLM endpoint.
    """
    raw_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                raw_text += text + "\n"
    return raw_text

# --- BATCH TEST BLOCK ---
if __name__ == "__main__":
    test_folder = "test_data"
    
    # If the folder doesn't exist yet, test in the current directory
    folder_to_scan = test_folder if os.path.exists(test_folder) else "."
    
    pdf_files = [f for f in os.listdir(folder_to_scan) if f.endswith(".pdf")]
    
    print(f"Found {len(pdf_files)} PDF(s) to process in '{folder_to_scan}':\n")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_to_scan, pdf_file)
        try:
            extracted_words = extract_text_and_coordinates(pdf_path)
            raw_text = get_raw_text_for_amd(pdf_path)
            
            print(f"✅ {pdf_file}:")
            print(f"   - Words indexed with bounding boxes: {len(extracted_words)}")
            print(f"   - Total characters extracted: {len(raw_text)}")
            
            # Sanity check: Ensure the PDF isn't a blank or scanned image
            if len(extracted_words) == 0:
                print("   ⚠️ WARNING: 0 words found! This PDF might be a scanned image without selectable text.")
        except Exception as e:
            print(f"   ❌ FAILED to process {pdf_file}: {e}")
        print("-" * 50) 