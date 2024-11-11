from flask import Flask, request, jsonify

from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from src.classifier import classify_file

app = Flask(__name__)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "xlsx", "xls", "docx", "txt"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


model = AutoModelForSequenceClassification.from_pretrained(
    "alex-apostolo/distilbert-base-uncased-fc"
)
tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()
torch.set_num_threads(1)


@app.route("/classify_file", methods=["POST"])
def classify_file_route():

    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"File type not allowed"}), 400

    file_class = classify_file(file, model, tokenizer, device)
    return jsonify({"file_class": file_class}), 200


if __name__ == "__main__":
    app.run(debug=True)
