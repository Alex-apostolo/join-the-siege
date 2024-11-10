from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)
from sklearn.model_selection import train_test_split
import pandas as pd
import torch
from torch.utils.data import Dataset
from config import BASE_PATH


class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer(
            text, truncation=True, padding="max_length", max_length=self.max_length
        )
        encoding["labels"] = torch.tensor(label, dtype=torch.long)
        return {key: torch.tensor(val) for key, val in encoding.items()}


def fine_tune_bert():
    # Load tokenizer and model
    model_name = "distilbert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=10
    )

    # Load dataset
    data = pd.read_csv(BASE_PATH / "combined_ocr.csv")  # Adjust path if necessary

    # Assume the CSV has columns 'text' and 'label'
    texts = data["text"].tolist()
    labels = data["type"].tolist()

    # Map labels to integers
    label_to_id = {label: idx for idx, label in enumerate(sorted(set(labels)))}
    int_labels = [label_to_id[label] for label in labels]

    # Split the data into train and validation sets
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, int_labels, test_size=0.2, random_state=42
    )

    # Create PyTorch datasets
    train_dataset = TextDataset(train_texts, train_labels, tokenizer)
    val_dataset = TextDataset(val_texts, val_labels, tokenizer)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./fine_tuned_bert",
        evaluation_strategy="epoch",
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        save_steps=500,
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    # Train and save the model
    trainer.train()
    trainer.save_model("./fine_tuned_bert")
    tokenizer.save_pretrained("./fine_tuned_bert")


if __name__ == "__main__":
    fine_tune_bert()
