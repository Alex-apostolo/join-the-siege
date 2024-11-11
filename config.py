from pathlib import Path
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

BASE_PATH = Path(__file__).resolve().parent
DATA_PATH = BASE_PATH / "synthetic_data" / "synthetic_data.csv"
MODEL_PATH = BASE_PATH / "model"
