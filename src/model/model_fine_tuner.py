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


class ModelFineTuner:
    def __init__(self, model_name="distilbert-base-uncased", data_path=DATA_PATH):
        self.model_name = model_name
        self.data_path = data_path
        self.id2label = {
            0: "drivers_license",
            1: "bank_statement",
            2: "invoice",
            3: "balance_sheet",
            4: "income_statement",
        }
        self.label2id = {v: k for k, v in self.id2label.items()}
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.accuracy_metric = evaluate.load("accuracy")

    def compute_metrics(self, eval_pred):
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return self.accuracy_metric.compute(predictions=predictions, references=labels)

    def tokenize(self, examples):
        return self.tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=256,
        )

    def preprocess(self):
        dataset = load_dataset("csv", data_files=str(self.data_path), split="train")
        dataset = dataset.rename_columns(
            {"generated_text": "text", "content_type": "labels"}
        )
        dataset = dataset.map(lambda x: {"labels": self.label2id[x["labels"]]})
        dataset = dataset.map(self.tokenize, batched=True)
        dataset = dataset.remove_columns("text")
        return dataset.train_test_split(0.2)

    def fine_tune(
        self, output_dir="distilbert-base-uncased-fc", epochs=3, batch_size=8
    ):
        dataset = self.preprocess()
        data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)

        model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=len(self.id2label),
            id2label=self.id2label,
            label2id=self.label2id,
        )

        training_args = TrainingArguments(
            output_dir=output_dir,
            eval_strategy="epoch",
            per_device_train_batch_size=batch_size,
            num_train_epochs=epochs,
            label_names=["labels"],
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset["train"],
            eval_dataset=dataset["test"],
            data_collator=data_collator,
            compute_metrics=self.compute_metrics,
        )

        trainer.train()
        trainer.push_to_hub()


if __name__ == "__main__":
    fine_tuner = ModelFineTuner()
    fine_tuner.fine_tune()
