import os
import argparse
from src.utils.config_loader import Config
from src.utils import config_loader
from src.utils.script_utils import validate_config
import importlib
from pathlib import Path


def train(args):
    config_file_path = args.config_file
    config = Config(config_file_path)

    # validate config
    validate_config(config)

    # set config globally
    config_loader.config = config

    # now visualize the dataset
    Model = importlib.import_module(f"src.{config.task}.model.models.{config.model}").Model


    model_dir = os.path.join("models",config.task,config.model)
    os.makedirs(model_dir,exist_ok=True)
    model_save_path = os.path.join(model_dir,"model.weights.h5")
    
    model = Model()
    model.train()
    model.save(model_save_path)
    metrics = model.evaluate()
    print("Model Evaluation Metrics:",metrics)

def main():
    parser = argparse.ArgumentParser(description="train model based on config yaml file")
    parser.add_argument("config_file",type=str)
    args = parser.parse_args()
    train(args)

if __name__=="__main__":
    main()