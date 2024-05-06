import os,shutil
import argparse

def create_file(file_path,file_content):
    with open(file_path,"w") as f:
        f.write(file_content)

def create_dataset(args):
    dataset_name = args.name
    force_flag = args.force
    datasets_dir = os.path.join('src','simple_regression_colorization','data','datasets')
    
    os.makedirs(datasets_dir,exist_ok=True)
    dataset_path = os.path.join(datasets_dir,dataset_name+".py")

    # deleted old dataset if force flag exists and dataset already exists
    if os.path.exists(dataset_path):
        if force_flag:
            print("Replacing existing dataset:",dataset_name)
            shutil.remove(dataset_path)
        else:
            print(f"{dataset_name} already exists, use --force flag if you want to reset it to default")
            exit()
    
    
    create_file(dataset_path,
"""# write dataset downloading preparation code in this file
# Note: download_prepare() this is specially choosen name so don't change this function's name
# you can add, remove and change any other function from this file

def download_prepare():
    \"\"\" function used to download dataset and apply 
        all type of data preprocessing required to prepare the dataset
    \"\"\"
    download_dataset()
    unzip_dataset()
    clean_dataset()
    move_dataset()
    

def download_dataset():
    \"\"\"download dataset\"\"\"
    pass
    
def unzip_dataset():
    \"\"\"unzip dataset(if required)\"\"\"
    pass
    
def clean_dataset():
    \"\"\"clean dataset(if required)\"\"\"
    pass

def move_dataset():
    \"\"\"move dataset to processed folder\"\"\"
    pass
""")

def main():
    parser = argparse.ArgumentParser(description="Create blueprint dataset")
    parser.add_argument('name',type=str,help="name of dataset (e.g., pascal-voc)")
    parser.add_argument("--force",action="store_true",help="forcefully replace old existing dataset to default",default=False)
    args = parser.parse_args()
    create_dataset(args)

if __name__=="__main__":
    main()
    
