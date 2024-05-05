from huggingface_hub import snapshot_download
import os,sys;sys.path.append(os.getcwd())
from src import config
from src.utils import *
import argparse
from pathlib import Path
from zipfile import ZipFile
from glob import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import shutil
from src.data.visualize_dataset import visualize_dataset

def download_dataset():
    """Used to download dataset from hugging face
    """
    print_title(f"Downloading {config.dataset} dataset from hugging face")
    snapshot_download(repo_id="Anuj-Panthri/Image-Colorization-Datasets",
                    repo_type="dataset",
                    local_dir=config.raw_dataset_dir,
                    allow_patterns=f"{config.dataset}/*")


def unzip_dataset():
    print_title(f"Unzipping dataset")
    print("Extracting to :",Path(config.interim_dataset_dir)/Path("trainval/"))
    with ZipFile(Path(config.raw_dataset_dir)/Path(f"{config.dataset}/trainval.zip"),"r") as zip:
        zip.extractall(Path(config.interim_dataset_dir)/Path("trainval/"))
    
    print("Extracting to :",Path(config.interim_dataset_dir)/Path("test/"))
    with ZipFile(Path(config.raw_dataset_dir)/Path(f"{config.dataset}/test.zip"),"r") as zip:
        zip.extractall(Path(config.interim_dataset_dir)/Path("test/")) 


def clean_dataset():
    print_title("CLEANING DATASET")
    trainval_dir = Path(config.interim_dataset_dir) / Path("trainval/")
    test_dir = Path(config.interim_dataset_dir) / Path("test/")

    trainval_paths = glob(str(trainval_dir/Path("*")))
    test_paths = glob(str(test_dir/Path("*")))

    print("train,test: ",len(trainval_paths),",",len(test_paths),sep="")
    
    
    def clean(image_paths,destination_dir):
        if os.path.exists(destination_dir): shutil.rmtree(destination_dir)
        os.makedirs(destination_dir)    
        for i in tqdm(range(len(image_paths))):
            img = cv2.imread(image_paths[i])
            img = cv2.resize(img,[128,128])
            if not is_bw(img):
                shutil.copy(trainval_paths[i],
                            destination_dir)
        print("saved to:",destination_dir)

    destination_dir = Path(config.processed_dataset_dir)/Path("trainval/")
    clean(trainval_paths,destination_dir)
    
    destination_dir = Path(config.processed_dataset_dir)/Path("test/")
    clean(test_paths,destination_dir)
    
    trainval_dir = Path(config.processed_dataset_dir) / Path("trainval/")
    test_dir = Path(config.processed_dataset_dir) / Path("test/")

    trainval_paths = glob(str(trainval_dir/Path("*")))
    test_paths = glob(str(test_dir/Path("*")))

    print("after cleaning train,test: ",len(trainval_paths),",",len(test_paths),sep="")


def prepare_dataset():
    print_title(f"Preparing dataset")
    download_dataset()
    unzip_dataset()
    clean_dataset()    

def delete_cache():
    ## clean old interim and raw datasets
    print_title("deleting unused raw and interim dataset dirs")
    if os.path.exists(config.raw_dataset_dir):
        shutil.rmtree(config.raw_dataset_dir)
    if os.path.exists(config.interim_dataset_dir):
        shutil.rmtree(config.interim_dataset_dir)

def delete_all():
    ## clean all datasets
    print_title("deleting all dataset dirs")
    if os.path.exists(config.raw_dataset_dir):
        shutil.rmtree(config.raw_dataset_dir)
    if os.path.exists(config.interim_dataset_dir):
        shutil.rmtree(config.interim_dataset_dir)
    if os.path.exists(config.processed_dataset_dir):
        shutil.rmtree(config.processed_dataset_dir)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("-d","--dataset",default="forests")
    parser.add_argument("--cache",action="store_true",default=True)
    parser.add_argument("--all",action="store_true")

    """
        prepare dataset:                      data prepare
        visualize dataset:                    data show
        delete raw & interim dataset dir:     data delete --cache
        delete all dataset dir:               data delete --all
    """
    
    args = parser.parse_args()
    # print(args)

    if args.command=="prepare":
        prepare_dataset()

    elif args.command=="show":
        visualize_dataset()

    elif args.command=="delete":
        if(args.all): delete_all()
        elif(args.cache): delete_cache()
    
    else:
        print("unsupported")

