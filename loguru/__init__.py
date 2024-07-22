import os
from pathlib import Path

HOME_DIR = str(Path.home())
LOGURU_DATA_DIR = os.path.join(HOME_DIR, '.loguru')
os.makedirs(LOGURU_DATA_DIR, exist_ok=True)
HUGGING_FACE_EMBEDDINGS_DEVICE_TYPE = 'cpu'
