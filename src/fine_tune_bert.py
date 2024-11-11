from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding,
)
import numpy as np
import evaluate
from datasets import load_dataset
from config import DATA_PATH

id2label = {
    0: "drivers_license",
    1: "bank_statement",
    2: "invoice",
    3: "balance_sheet",
    4: "income_statement",
}
label2id = {v: k for k, v in id2label.items()}

accuracy_metric = evaluate.load("accuracy")


def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy_metric.compute(predictions=predictions, references=labels)


model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)


def tokenize(examples):
    tokens = tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=128,
    )
    return tokens


def preprocess(path):
    dataset = load_dataset("csv", data_files=path, split="train")
    dataset = dataset.rename_columns(
        {"generated_text": "text", "content_type": "labels"}
    )
    dataset = dataset.map(lambda x: {"labels": label2id[x["labels"]]})
    dataset = dataset.map(tokenize, batched=True)
    dataset = dataset.remove_columns("text")
    dataset = dataset.train_test_split(0.2)
    return dataset


def fine_tune_bert():
    dataset = preprocess(str(DATA_PATH))

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    trainer = Trainer(
        model=AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=len(id2label),
            id2label=id2label,
            label2id=label2id,
        ),
        args=TrainingArguments(
            output_dir="distilbert-base-uncased-fc",
            eval_strategy="epoch",
            per_device_train_batch_size=8,
            num_train_epochs=3,
            label_names=["labels"],
        ),
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    trainer.push_to_hub()


if __name__ == "__main__":
    fine_tune_bert()
