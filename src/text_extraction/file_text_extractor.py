from PIL import Image
from pdf2image import convert_from_bytes
from pytesseract import image_to_string
from docx import Document
import pandas as pd
from pypdf import PdfReader


class FileTextExtractor:
    def __init__(self):
        self.custom_config = r"--oem 1 --psm 3"  # OCR configuration for Tesseract

    def ocr_image(self, image):
        return image_to_string(image, config=self.custom_config)

    def extract_text(self, file_stream, file_extension):
        if file_extension == ".pdf":
            return self.extract_pdf_text(file_stream)

        elif file_extension in [".jpg", ".jpeg", ".png"]:
            return self.extract_image_text(file_stream)

        elif file_extension == ".docx":
            return self.extract_docx_text(file_stream)

        elif file_extension == ".txt":
            return self.extract_txt_text(file_stream)

        elif file_extension in [".xls", ".xlsx"]:
            return self.extract_excel_text(file_stream)

        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")

    def extract_pdf_text(self, file_stream):
        try:
            pdf_reader = PdfReader(file_stream)
            text = "".join(
                page.extract_text() for page in pdf_reader.pages if page.extract_text()
            )
        except Exception:
            text = ""

        if not text.strip():
            file_stream.seek(0)
            images = convert_from_bytes(file_stream.read())
            text = "\n".join(self.ocr_image(image) for image in images)
        return text

    def extract_image_text(self, file_stream):
        image = Image.open(file_stream)
        return self.ocr_image(image)

    def extract_docx_text(self, file_stream):
        file_stream.seek(0)
        doc = Document(file_stream)
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
        return text

    def extract_txt_text(self, file_stream):
        file_stream.seek(0)
        return file_stream.read().decode("utf-8")

    def extract_excel_text(self, file_stream):
        file_stream.seek(0)
        excel_data = pd.read_excel(file_stream, sheet_name=None)
        text = ""
        for sheet_name, sheet_data in excel_data.items():
            text += f"\nSheet: {sheet_name}\n"
            text += sheet_data.to_string(index=False, header=True)
        return text
