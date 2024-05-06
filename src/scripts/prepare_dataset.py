import argparse
from src.utils.config_loader import Config
from src.utils import config_loader
from src.utils.script_utils import validate_config
import importlib


def prepare_dataset(args):
    config_file_path = args.config_file
    config = Config(config_file_path)

    # validate config
    validate_config(config)

    # set config globally
    config_loader.config = config

    # now prepare the dataset
    download_prepare = importlib.import_module(f"src.{config.task}.data.datasets.{config.dataset}").download_prepare
    print("Preparing dataset")
    download_prepare()
    print("Prepared dataset")

def main():
    parser = argparse.ArgumentParser(description="Prepare dataset based on config yaml file")
    parser.add_argument("config_file",type=str)
    args = parser.parse_args()
    prepare_dataset(args)

if __name__=="__main__":
    main()