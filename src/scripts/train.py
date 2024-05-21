import os,shutil
import argparse
from comet_ml import Experiment
from src.utils.config_loader import Config
from src.utils import config_loader
from src.utils.data_utils import print_title
from src.utils.script_utils import validate_config
import importlib
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

def train(args):
    config_file_path = args.config_file
    config = Config(config_file_path)

    # validate config
    validate_config(config)

    # set config globally
    config_loader.config = config

    # now load the model
    Model = importlib.import_module(f"src.{config.task}.model.models.{config.model}").Model


    model_dir = os.path.join("models",config.task,config.model)
    os.makedirs(model_dir,exist_ok=True)
    model_save_path = os.path.join(model_dir,"model.weights.h5")
    
    # save config to exported model folder
    shutil.copy(config_file_path,model_dir)

    experiment = Experiment(
        api_key=os.environ["COMET_API_KEY"],
        project_name="image-colorization",
        workspace="anujpanthri",
        auto_histogram_activation_logging=True,
        auto_histogram_epoch_rate=True,
        auto_histogram_gradient_logging=True,
        auto_histogram_weight_logging=True,
        auto_param_logging=True,
    )

    model = Model(experiment=experiment)
    model.train()
    model.save(model_save_path)
    
    # log model to comet
    if "LOCAL_SYSTEM" not in os.environ:
        experiment.log_model(f"{config.task}_{config.dataset}_{config.model}",model_dir)

    # evaluate model
    print_title("\nEvaluating Model")
    metrics = model.evaluate()
    print("Model Evaluation Metrics:",metrics)
    
    experiment.end()

def main():
    parser = argparse.ArgumentParser(description="train model based on config yaml file")
    parser.add_argument("config_file",type=str)
    args = parser.parse_args()
    train(args)

if __name__=="__main__":
    main()