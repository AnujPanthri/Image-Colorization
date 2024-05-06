import os,shutil
import argparse

def create_file(file_path,file_content):
    with open(file_path,"w") as f:
        f.write(file_content)
            
def create_data(data_dir,dataset_name,sub_task_dir):
    # call src/sub_task/scripts/create_dataset.py dataset_name
    os.system(f"python {sub_task_dir}/scripts/create_dataset.py {dataset_name}")

    register_datasets_file_path = os.path.join(data_dir,"register_datasets.py")
    create_file(register_datasets_file_path,
f"""# register your datasets here

datasets = ["{dataset_name}"]

""")



def create_model(model_dir:str, model_name:str, sub_task_dir:str):
    base_model_interface_path = os.path.join(model_dir,"base_model_interface.py")
    
    create_file(base_model_interface_path,
"""import numpy as np
from abc import ABC, abstractmethod

# BaseModel Abstract class
# all the models within this sub_task must inherit this class

class BaseModel(ABC):
    @abstractmethod
    def train(self):
        pass
        
    @abstractmethod        
    def predict(self,inputs):
        pass
""")


    # call src/sub_task/scripts/create_model.py model_name
    os.system(f"python {sub_task_dir}/scripts/create_model.py {model_name}")
    

    register_models_path = os.path.join(model_dir,"register_models.py")
    create_file(register_models_path,
f"""# register models of this sub_task here
models = ["{model_name}"]
""")

    
    
    losses_path = os.path.join(model_dir,"losses.py")
    create_file(losses_path,
"""# define loss functions here
""")

    metrics_path = os.path.join(model_dir,"metrics.py")
    create_file(metrics_path,
"""# define metrics here
""")
    
    callbacks_path = os.path.join(model_dir,"callbacks.py")
    create_file(callbacks_path,
"""# define callbacks here
""")
    
    dataloaders_path = os.path.join(model_dir,"dataloaders.py")
    create_file(dataloaders_path,
"""# define dataloaders here
""")
    

def create_scripts(scripts_dir,sub_task):
    create_dataset_path = os.path.join(scripts_dir,"create_dataset.py")
    create_file(create_dataset_path,
f"""import os,shutil
import argparse

def create_file(file_path,file_content):
    with open(file_path,"w") as f:
        f.write(file_content)

def create_dataset(args):
    dataset_name = args.name
    force_flag = args.force
    datasets_dir = os.path.join('src','{sub_task}','data','datasets')
    
    os.makedirs(datasets_dir,exist_ok=True)
    dataset_path = os.path.join(datasets_dir,dataset_name+".py")

    # deleted old dataset if force flag exists and dataset already exists
    if os.path.exists(dataset_path):
        if force_flag:
            print("Replacing existing dataset:",dataset_name)
            shutil.remove(dataset_path)
        else:
            print(f"{{dataset_name}} already exists, use --force flag if you want to reset it to default")
            exit()
    
    
    create_file(dataset_path,
\"\"\"# write dataset downloading preparation code in this file
# Note: download_prepare() this is specially choosen name so don't change this function's name
# you can add, remove and change any other function from this file

def download_prepare():
    \\"\\"\\" function used to download dataset and apply 
        all type of data preprocessing required to prepare the dataset
    \\"\\"\\"
    download_dataset()
    unzip_dataset()
    clean_dataset()
    move_dataset()
    

def download_dataset():
    \\"\\"\\"download dataset\\"\\"\\"
    pass
    
def unzip_dataset():
    \\"\\"\\"unzip dataset(if required)\\"\\"\\"
    pass
    
def clean_dataset():
    \\"\\"\\"clean dataset(if required)\\"\\"\\"
    pass

def move_dataset():
    \\"\\"\\"move dataset to processed folder\\"\\"\\"
    pass
\"\"\")

def main():
    parser = argparse.ArgumentParser(description="Create blueprint dataset")
    parser.add_argument('name',type=str,help="name of dataset (e.g., pascal-voc)")
    parser.add_argument("--force",action="store_true",help="forcefully replace old existing dataset to default",default=False)
    args = parser.parse_args()
    create_dataset(args)

if __name__=="__main__":
    main()
    
""")
    
    create_model_path = os.path.join(scripts_dir,"create_model.py")
    create_file(create_model_path,
f"""import os,shutil
import argparse

def create_file(file_path,file_content):
    with open(file_path,"w") as f:
        f.write(file_content)

def create_model(args):
    model_name = args.name
    force_flag = args.force
    models_dir = os.path.join('src','{sub_task}','model',"models")
    os.makedirs(models_dir,exist_ok=True)
    model_path = os.path.join(models_dir,model_name+".py")

    # deleted old model if force flag exists and model already exists
    if os.path.exists(model_path):
        if force_flag:
            print("Replacing existing model:",model_name)
            shutil.remove(model_path)
        else:
            print(f"{{model_name}} already exists, use --force flag if you want to reset it to default")
            exit()

    
    model_name_camel_case = "".join([part.capitalize() for part in model_name.split("_")])
    create_file(model_path,
f\"\"\"from src.{sub_task}.model.base_model_interface import BaseModel

class Model(BaseModel):
    def train(self):
        pass
        
    def predict(self,inputs):
        pass
\"\"\")
    
def main():
    parser = argparse.ArgumentParser(description="Create blueprint model")
    parser.add_argument('name',type=str,help="name of model (e.g., model_v2)")
    parser.add_argument("--force",action="store_true",help="forcefully replace old existing model to default",default=False)
    args = parser.parse_args()
    create_model(args)

if __name__=="__main__":
    main()
    
""")
    
    

def create_sub_task(args):
    """Used to create sub_task within our main task"""
    sub_task = args.sub_task
    force_flag = args.force
    dataset_name = "dataset1"
    model_name = "model1"

    sub_task_dir = os.path.join('src',sub_task)
    data_dir = os.path.join(sub_task_dir,'data')
    model_dir = os.path.join(sub_task_dir,'model')
    scripts_dir = os.path.join(sub_task_dir,"scripts")
    # print(scripts_dir)
    # deleted old sub_task if force flag exists and sub_task already exists
    if os.path.exists(sub_task_dir):
        if force_flag:
            print("Replacing existing sub_task:",sub_task)
            shutil.rmtree(sub_task_dir)
        else:
            print(f"{sub_task} already exists, use --force flag if you want to reset it to default")
            exit()

    # create empty folders
    os.makedirs(sub_task_dir,exist_ok=True)
    os.makedirs(data_dir,exist_ok=True)
    os.makedirs(model_dir,exist_ok=True)
    os.makedirs(scripts_dir,exist_ok=True)

    # make config validator file
    validate_config_file_path = os.path.join(sub_task_dir,"validate_config.py")
    create_file(validate_config_file_path,
'''# from cerberus import Validator

# write config file schema here
# based on cerberus Validator

schema = {
    "seed": {
        "type": "integer",
    },
    "image_size": {"type": "integer", "required": True},
    "train_size": {"type": "float", "required": True},
    "shuffle": {"type": "boolean", "required": True},
    "batch_size": {
        "type": "integer",
        "required": True,
    },
    "epochs": {
        "type": "integer",
        "required": True,
    },
}

''')
    
    # make scripts files
    create_scripts(scripts_dir,sub_task)

    # make data files
    create_data(data_dir,dataset_name,sub_task_dir)

    # make model files
    create_model(model_dir,model_name,sub_task_dir)

    
def main():
    parser = argparse.ArgumentParser(description="Create blueprint sub_task")
    parser.add_argument('sub_task',type=str,help="sub_task of project (e.g., simple_regression_colorization)")
    parser.add_argument("--force",action="store_true",help="forcefully replace old existing sub_task to default",default=False)
    args = parser.parse_args()

    create_sub_task(args)

if __name__=="__main__":
    main()
    