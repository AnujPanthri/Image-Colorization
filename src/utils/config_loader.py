import yaml
from pathlib import Path
import random
import tensorflow as tf
import numpy as np
import os

class Config:
    def __init__(self,config_file_path:str):
        """loads config from config_file_path"""
        with open(config_file_path,"r") as f:
            self.config_dict = yaml.safe_load(f)
    
    def __str__(self):
        return str(self.config_dict)

    def __getattr__(self,name):
        return self.config_dict.get(name)


# exports constants
constants = Config("constants.yaml")
constants.config_dict['RAW_DATASET_DIR'] = Path(constants.config_dict['RAW_DATASET_DIR'])
constants.config_dict['INTERIM_DATASET_DIR'] = Path(constants.config_dict['INTERIM_DATASET_DIR'])
constants.config_dict['PROCESSED_DATASET_DIR'] = Path(constants.config_dict['PROCESSED_DATASET_DIR'])

config = None


def set_seed(seed: int = 42) -> None:
  random.seed(seed)
  np.random.seed(seed)
  tf.random.set_seed(seed)
  tf.experimental.numpy.random.seed(seed)

  # When running on the CuDNN backend, two further options must be set
  os.environ['TF_CUDNN_DETERMINISTIC'] = '1'
  os.environ['TF_DETERMINISTIC_OPS'] = '1'
  # Set a fixed value for the hash seed
  os.environ["PYTHONHASHSEED"] = str(seed)
  print(f"Random seed set as {seed}")
