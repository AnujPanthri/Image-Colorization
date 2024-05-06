import yaml
from pathlib import Path

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