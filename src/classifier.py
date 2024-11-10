from werkzeug.datastructures import FileStorage
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from src.file_text_extractor import extract_text
import os
from io import BytesIO
from config import BASE_PATH

def classify_file(file: FileStorage):
    file_extension = os.path.splitext(file.filename)[1].lower()
    file_stream = BytesIO(file.read())  # Read file content into a byte stream
    text = extract_text(
        file_stream, file_extension
    )  # Pass the stream and extension to extract_text
    print(text)

    model_path = BASE_PATH / "fine_tuned_bert"
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    # Run the model to get outputs
    outputs = model(**inputs)

    # Extract logits and get the predicted class
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return predicted_class
