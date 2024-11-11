import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class ModelInference:
    def __init__(
        self, model_name="alex-apostolo/distilbert-base-uncased-fc", device=None
    ):
        self.device = device or torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(
            "distilbert/distilbert-base-uncased"
        )

        self.model.to(self.device)
        self.model.eval()
        torch.set_num_threads(1)

    def predict(self, text):
        inputs = self.tokenizer(
            text, return_tensors="pt", padding=True, truncation=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        predicted_class_id = logits.argmax().item()
        predicted_class = self.model.config.id2label[predicted_class_id]

        return predicted_class
