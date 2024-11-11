from werkzeug.datastructures import FileStorage
from src.file_text_extractor import extract_text
import os
from io import BytesIO
import torch


def classify_file(file: FileStorage, model, tokenizer, device):
    file_extension = os.path.splitext(file.filename)[1].lower()
    file_stream = BytesIO(file.read())
    text = extract_text(file_stream, file_extension)

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(
        device
    )
    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_class_id = logits.argmax().item()
    predicted_class = model.config.id2label[predicted_class_id]
    return predicted_class
