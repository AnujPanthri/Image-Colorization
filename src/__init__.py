from src.utils import Config
from pathlib import Path

config = Config("config.yaml")
# config.raw_dataset_dir = Path(config.raw_dataset_dir)
# config.interim_dataset_dir = Path(config.interim_dataset_dir)
# config.processed_dataset_dir = Path(config.processed_dataset_dir)

# print(config)