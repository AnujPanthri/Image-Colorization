import os
import argparse
from src.utils.config_loader import Config
from src.utils import config_loader
from src.utils.script_utils import validate_config
import importlib


def visualize_dataset(args):
    config_file_path = args.config_file
    config = Config(config_file_path)

    # validate config
    validate_config(config)

    # set config globally
    config_loader.config = config

    # now load model and visualize the results
    model_dir = os.path.join("models",config.task,config.model)
    model_save_path = os.path.join(model_dir,"model.weights.h5")

    if not os.path.exists(model_save_path):
        raise Exception("No model found:","first use train.py to train and export a model")
    
    Model = importlib.import_module(f"src.{config.task}.model.models.{config.model}").Model
    model = Model(model_save_path)

    # model.train_ds
    model.show_results()
    
    

def main():
    parser = argparse.ArgumentParser(description="Prepare dataset based on config yaml file")
    parser.add_argument("config_file",type=str)
    args = parser.parse_args()
    visualize_dataset(args)

if __name__=="__main__":
    main()