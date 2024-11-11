from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding,
)
import pandas as pd
import numpy as np
import evaluate
import json
from datasets import Dataset
from config import DATA_PATH, MODEL_PATH

# Define label mappings
id2label = {
    0: "drivers_license",
    1: "bank_statement",
    2: "invoice",
    3: "balance_sheet",
    4: "income_statement",
}
label2id = {v: k for k, v in id2label.items()}


# Utility function to split the dataset
def load_and_split_dataset(test_size=0.2):
    data = pd.read_csv(DATA_PATH)
    data["labels"] = data["content_type"].map(label2id)
    del data["content_type"]

    dataset = Dataset.from_pandas(data)
    split_data = dataset.train_test_split(test_size=test_size)
    return split_data["train"], split_data["test"]


# Utility function for tokenizing datasets
def preprocess_data(tokenizer, dataset):
    def preprocess_function(examples):
        return tokenizer(
            examples["generated_text"], padding="max_length", truncation=True
        )

    tokenized_data = dataset.map(preprocess_function, batched=True)
    tokenized_data.set_format(
        type="torch", columns=["input_ids", "attention_mask", "labels"]
    )
    return tokenized_data


# Compute accuracy metrics
accuracy_metric = evaluate.load("accuracy")


def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy_metric.compute(predictions=predictions, references=labels)


# Save metrics to file
def save_metrics(metrics, path, filename):
    with open(path / filename, "w") as f:
        json.dump(metrics, f)


# Main training and evaluation function
def fine_tune_bert():
    model_name = "distilbert-base-uncased"
    train_dataset, val_dataset = load_and_split_dataset()

    # Load tokenizer and preprocess datasets
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenized_train = preprocess_data(tokenizer, train_dataset)
    tokenized_val = preprocess_data(tokenizer, val_dataset)

    # Data collator
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # Initialize the Trainer
    trainer = Trainer(
        model=AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=len(id2label),
            id2label=id2label,
            label2id=label2id,
        ),
        args=TrainingArguments(
            output_dir=str(MODEL_PATH),
            eval_strategy="epoch",
            per_device_train_batch_size=8,
            num_train_epochs=3,
        ),
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    # Train and save the model
    train_result = trainer.train()
    trainer.save_model(MODEL_PATH)
    tokenizer.save_pretrained(MODEL_PATH)

    # Save training and evaluation metrics
    save_metrics(train_result.metrics, MODEL_PATH, "train_metrics.json")
    eval_metrics = trainer.evaluate()
    save_metrics(eval_metrics, MODEL_PATH, "eval_metrics.json")


if __name__ == "__main__":
    fine_tune_bert()
