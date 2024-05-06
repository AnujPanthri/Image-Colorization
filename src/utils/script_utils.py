from cerberus import Validator
import importlib
import os

def validate_config(config):
    basic_schema = {
        "task": {
            "type":"string",
            "required":True
        },
        "dataset": {
            "type":"string",
            "required":True
        },
        "model": {
            "type":"string",
            "required":True
        },
    }
    basic_v = Validator(basic_schema,allow_unknown=True)
    
    if not basic_v.validate(config.config_dict):
        raise Exception(f"Invalid config file:",basic_v.errors)
    
    # check if such task exists
    if not os.path.exists(os.path.join("src",config.task)):
        raise Exception("Invalid config file:",f"no such task {config.task}")

    # check if valid dataset
    all_datasets = importlib.import_module(f"src.{config.task}.data.register_datasets").datasets
    if config.dataset not in all_datasets:
        raise Exception("Invalid config file:",f"no {config.dataset} dataset found in registered datasets: {all_datasets}")
    
    # check if valid model
    all_models = importlib.import_module(f"src.{config.task}.model.register_models").models
    if config.model not in all_models:
        raise Exception("Invalid config file:",f"no {config.model} model found in registered models: {all_models}")
    
    
    
    # check the sub_task's validate_config schema
    task_schema = importlib.import_module(f"src.{config.task}.validate_config").schema
    sub_task_v = Validator(task_schema,allow_unknown=True)

    if not sub_task_v.validate(config.config_dict):
        raise Exception(f"Invalid config file:",sub_task_v.errors)
    
