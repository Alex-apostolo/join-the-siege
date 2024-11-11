from werkzeug.datastructures import FileStorage
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from src.file_text_extractor import extract_text
import os
from io import BytesIO


def classify_file(file: FileStorage):
    file_extension = os.path.splitext(file.filename)[1].lower()
    file_stream = BytesIO(file.read())  # Read file content into a byte stream
    text = extract_text(
        file_stream, file_extension
    )  # Pass the stream and extension to extract_text
    print(text)

    model = AutoModelForSequenceClassification.from_pretrained(
        "alex-apostolo/distilbert-base-uncased-fc"
    )
    tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased")
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    # Run the model to get outputs
    outputs = model(**inputs)

    # Extract logits and get the predicted class
    logits = outputs.logits
    predicted_class_id = logits.argmax().item()
    predicted_class = model.config.id2label[predicted_class_id]
    return predicted_class
