import os
from io import BytesIO
from src.text_extraction.file_text_extractor import FileTextExtractor
from src.model.model_inference import ModelInference


def classify_file(file):
    file_extension = os.path.splitext(file.filename)[1].lower()
    file_stream = BytesIO(file.read())

    text_extractor = FileTextExtractor()
    text = text_extractor.extract_text(file_stream, file_extension)

    model_inference = ModelInference()
    predicted_class = model_inference.predict(text)

    return predicted_class
