from PIL import Image
from pdf2image import convert_from_bytes
from pytesseract import image_to_string
from docx import Document
import pandas as pd
from concurrent.futures import ProcessPoolExecutor


def ocr_image(image):
    custom_config = r"--oem 1 --psm 3"
    return image_to_string(image, config=custom_config)


def extract_text(file_stream, file_extension):
    if file_extension == ".pdf":
        # Convert PDF to images
        images = convert_from_bytes(file_stream.read())

        # Process each page image in parallel using OCR
        with ProcessPoolExecutor() as executor:
            ocr_results = list(executor.map(ocr_image, images))

        # Combine text from all pages
        text = "\n".join(ocr_results)
        return text

    elif file_extension in [".jpg", ".jpeg", ".png"]:
        image = Image.open(file_stream)
        return image_to_string(image)

    elif file_extension == ".docx":
        file_stream.seek(0)
        doc = Document(file_stream)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text

    elif file_extension == ".txt":
        file_stream.seek(0)
        return file_stream.read().decode("utf-8")

    elif file_extension in [".xls", ".xlsx"]:
        file_stream.seek(0)
        excel_data = pd.read_excel(file_stream, sheet_name=None)
        text = ""
        for sheet_name, sheet_data in excel_data.items():
            text += f"\nSheet: {sheet_name}\n"
            text += sheet_data.to_string(index=False, header=True)
        return text

    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")
