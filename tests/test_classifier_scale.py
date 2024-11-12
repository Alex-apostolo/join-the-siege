import requests
from io import BytesIO
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from config import DATA_PATH

URL = "http://127.0.0.1:8000/classify_file"
NUM_DOCUMENTS = 1000
WORKERS = 100

data = pd.read_csv(DATA_PATH)
if len(data) < NUM_DOCUMENTS:
    data = pd.concat(
        [data] * (NUM_DOCUMENTS // len(data) + 1), ignore_index=True
    ).sample(n=NUM_DOCUMENTS)
data = data.head(NUM_DOCUMENTS)


def upload_document(row):
    content = "\n".join([f"{col}: {val}" for col, val in row.items()])
    file_stream = BytesIO(content.encode("utf-8"))
    response = requests.post(
        URL, files={"file": ("dummy.txt", file_stream)}, timeout=50
    )
    if response.ok:
        return {
            "filename": "dummy.txt",
            "file_class": response.json().get("file_class"),
        }
    else:
        return {"filename": "dummy.txt", "error": response.text}


with ThreadPoolExecutor(max_workers=WORKERS) as executor:
    results = list(executor.map(upload_document, [row for _, row in data.iterrows()]))

print(f"Total files processed: {len(results)}")
print(results)
