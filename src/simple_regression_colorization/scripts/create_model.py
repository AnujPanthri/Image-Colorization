import os,shutil
import argparse

def create_file(file_path,file_content):
    with open(file_path,"w") as f:
        f.write(file_content)

def create_model(args):
    model_name = args.name
    force_flag = args.force
    models_dir = os.path.join('src','simple_regression_colorization','model',"models")
    os.makedirs(models_dir,exist_ok=True)
    model_path = os.path.join(models_dir,model_name+".py")

    # deleted old model if force flag exists and model already exists
    if os.path.exists(model_path):
        if force_flag:
            print("Replacing existing model:",model_name)
            shutil.remove(model_path)
        else:
            print(f"{model_name} already exists, use --force flag if you want to reset it to default")
            exit()

    
    model_name_camel_case = "".join([part.capitalize() for part in model_name.split("_")])
    create_file(model_path,
f"""from src.simple_regression_colorization.model.base_model_interface import BaseModel

class Model(BaseModel):
    def train(self):
        pass
        
    def predict(self,inputs):
        pass
""")
    
def main():
    parser = argparse.ArgumentParser(description="Create blueprint model")
    parser.add_argument('name',type=str,help="name of model (e.g., model_v2)")
    parser.add_argument("--force",action="store_true",help="forcefully replace old existing model to default",default=False)
    args = parser.parse_args()
    create_model(args)

if __name__=="__main__":
    main()
    
