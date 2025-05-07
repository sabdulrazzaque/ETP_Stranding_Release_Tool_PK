from PIL import Image
import pytesseract
import logging
import re

# Set tesseract.exe path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_file):
    try:
        image = Image.open(image_file).convert("RGB")
        return pytesseract.image_to_string(image, lang='eng+urd').strip()
    except Exception as e:
        logging.error(f"OCR failed: {e}")
        return ""

def clean_post_content(text):
    text = re.sub(r'[\u0000-\u001F©@™\u2022\u2192~»—“”…]', '', text)
    return re.sub(r'\s+', ' ', text).strip()
