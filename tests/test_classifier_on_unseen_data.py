import os
import requests
from concurrent.futures import ProcessPoolExecutor
from config import BASE_PATH
from pathlib import Path

URL = "http://127.0.0.1:8000/classify_file"
FOLDER_PATH = BASE_PATH / "files"


def upload_file(file_path: Path):
    with open(file_path, "rb") as f:
        response = requests.post(URL, files={"file": f})
        return (
            {file_path.name: response.json()["file_class"]}
            if response.ok
            else {"filename": file_path.name, "error": response.text}
        )


def upload_files_in_parallel():
    file_paths = [
        file_path
        for file_path in FOLDER_PATH.iterdir()
        if file_path.is_file() and not file_path.name.startswith(".")
    ]
    with ProcessPoolExecutor() as executor:  # Use ProcessPoolExecutor instead of ThreadPoolExecutor
        results = list(executor.map(upload_file, file_paths))
    return results


if __name__ == "__main__":
    result = upload_files_in_parallel()
    print(result)
