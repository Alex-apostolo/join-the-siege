from PIL import Image
from pdf2image import convert_from_bytes
from pytesseract import image_to_string
from docx import Document


def extract_text(file_stream, file_extension):
    if file_extension == ".pdf":
        # Convert PDF byte stream to images and apply OCR
        text = ""
        images = convert_from_bytes(file_stream.read())  # Convert directly from bytes
        for image in images:
            text += image_to_string(image)
        return text

    elif file_extension in [".jpg", ".jpeg", ".png"]:
        # Open image from byte stream and apply OCR
        image = Image.open(file_stream)
        return image_to_string(image)

    elif file_extension == ".docx":
        # Read DOCX from byte stream
        file_stream.seek(0)
        doc = Document(file_stream)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text

    elif file_extension == ".txt":
        # Read text file from byte stream
        file_stream.seek(0)
        return file_stream.read().decode("utf-8")

    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")
