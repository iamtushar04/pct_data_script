import deep_translator.exceptions
import fitz  # PyMuPDF
import pytesseract
import os, re
from PIL import Image
from typing import Tuple
from deep_translator import GoogleTranslator
from const import LANG_MAP
from os_operations import get_latest_pdf, remove_file
from source.text_extraction import extract_agent_info, extract_applicant_info, extract_email, extract_phone

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\jaswa\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = 'C:\\Users\\jaswa\\AppData\\Local\\Programs\\Tesseract-OCR\\tessdata\\'


def convert_pdf2img(input_file: str, pages: Tuple = None):
    """Converts pdf to image and generates a file by page"""
    # Open the document
    pdfIn = fitz.open(input_file)
    output_files = []
    # Iterate throughout the pages

    for pg in range(pdfIn.page_count):
        if str(pages) != str(None):
            if str(pg) not in str(pages):
                continue
        # Select a page
        page = pdfIn[pg]
        rotate = int(0)
        zoom_x = 2
        zoom_y = 2
        # The zoom factor is equal to 2 in order to make text clear
        # Pre-rotate is to rotate if needed.
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        output_file = f"{os.path.splitext(os.path.basename(input_file))[0]}_page{pg + 1}.png"

        pix.save(output_file)
        output_files.append(output_file)
    pdfIn.close()
    return output_files


def extract_text_from_image(image_bytes):
    image = Image.open(image_bytes)
    text = pytesseract.image_to_string(image)
    return text


def translate_text_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except deep_translator.exceptions.RequestError as e:
        print("Failed to translate due to API Connection Error")
        return text

def ocr_image(image_path, lang='eng'):
    try:
        return pytesseract.image_to_string(Image.open(image_path), lang=lang, config=r'--oem 1 --psm 6')
    except pytesseract.pytesseract.TesseractError:
        return f"Failed to load language {lang}"


def detect_lang_of_img_text(image_path):
    detect_lang = pytesseract.image_to_osd(image_path, output_type=pytesseract.Output.DICT).get('script')
    return LANG_MAP[detect_lang]


def detect_image_lang(img_path):
    try:
        osd = pytesseract.image_to_osd(img_path)
        script = re.search("Script: ([a-zA-Z]+)\n", osd).group(1)
        conf = re.search("Script confidence: (\d+\.?(\d+)?)", osd).group(1)
        return script, float(conf)
    except:
        return None, 0.0


def pdf_images_to_text(file_path, lang: str = "eng"):
    lang = "eng" if lang is None else f"{lang}+eng"
    print(f"**************************************************************language: {lang}")
    pdf_path = get_latest_pdf(file_path)
    images = convert_pdf2img(pdf_path)
    data = ""
    for file_ in images:
        extract_text = ocr_image(file_, lang=lang)
        if lang == "eng+eng":
            data += extract_text
        else:
            data += translate_text_to_english(extract_text[:4999])
        remove_file(file_)
    remove_file(pdf_path)
    return data


def extract_ocr_data(file_path, lang: str = None):
    data = pdf_images_to_text(file_path, lang)
    agent_info = extract_agent_info(data)
    applicant_info = extract_applicant_info(data)
    email = extract_email(data.replace(". ", ".").replace(" .", ".").replace("@ ", "@").replace(" @", "@"))
    phone = extract_phone(data)
    return {'Applicant_info': applicant_info, 'Agent_info': agent_info, 'Email': email, 'Phone': phone}
