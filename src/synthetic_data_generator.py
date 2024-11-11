import os
import pandas as pd
import logging
from openai import OpenAI
from dotenv import load_dotenv
from config import DATA_PATH
from pathlib import Path
import random

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
output_path = DATA_PATH / "synthetic_data.csv"

content_types = {
    "drivers_license": "generate the text content of a realistic drivers license",
    "bank_statement": "generate the text content of a realistic bank statement",
    "invoice": "generate the text content of a realistic invoice",
    "balance_sheet": "generate the text content of a realistic balance sheet",
    "income_statement": "generate the text content of a realistic income statement",
}

prompt = "Exclude conversational or descriptive text; use synonyms or abbreviations; return only the text without any formatting."


def generate_completion(content_prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content_prompt},
            ],
            temperature=1,
            max_tokens=200,
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating text for '{content_prompt}': {e}")
        return None


def generate_synthetic_data(content_types, num_examples=50):
    existing_data = (
        pd.read_csv(output_path)
        if Path(output_path).exists()
        else pd.DataFrame(columns=["content_type", "generated_text"])
    )
    needed_examples = {
        k: num_examples - existing_data[existing_data["content_type"] == k].shape[0]
        for k in content_types
    }
    new_data = [
        {
            "content_type": name,
            "generated_text": apply_ocr_mutations(generate_completion(prompt)),
        }
        for name, prompt in content_types.items()
        for _ in range(needed_examples[name])
        if needed_examples[name] > 0
    ]

    if new_data:
        pd.concat([existing_data, pd.DataFrame(new_data)], ignore_index=True).to_csv(
            output_path, index=False
        )
        logging.info(f"Data saved to {output_path}")
    else:
        logging.info("CSV is up-to-date.")


def apply_ocr_mutations(text):
    text = "".join((char + " " if random.random() < 0.1 else char) for char in text)
    text = "".join(char for char in text if random.random() > 0.05)
    return text


if __name__ == "__main__":
    generate_synthetic_data(content_types, num_examples=50)
