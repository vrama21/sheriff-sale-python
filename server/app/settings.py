import os
from pathlib import Path

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = os.environ.get("PORT", "5000")

BASE_DIR = Path(__file__).resolve().parent