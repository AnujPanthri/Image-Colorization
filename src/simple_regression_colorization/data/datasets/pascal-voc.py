from src.utils.data_utils import download_personal_hf_dataset,unzip_file,is_bw,print_title
from zipfile import ZipFile
from pathlib import Path
from src.utils.config_loader import constants,config
from glob import glob
import shutil,os
from tqdm import tqdm
import cv2



# write dataset downloading preparation code in this file
# Note: download_prepare() this is specially choosen name so don't change this function's name
# you can add, remove and change any other function from this file

def download_prepare():
    """ function used to download dataset and apply 
        all type of data preprocessing required to prepare the dataset
    """
    download_dataset()
    unzip_dataset()
    clean_dataset()
    

def download_dataset():
    """Used to download dataset from hugging face"""
    print_title(f"Downloading forests dataset from hugging face")
    # download_hf_dataset("")
    download_personal_hf_dataset("pascal-voc")
    


def unzip_dataset():
    print_title(f"Unzipping dataset")
    
    unzip_file(constants.RAW_DATASET_DIR/Path("pascal-voc/trainval.zip"),
               constants.INTERIM_DATASET_DIR/Path("trainval/"))
    
    unzip_file(constants.RAW_DATASET_DIR/Path("pascal-voc/test.zip"),
               constants.INTERIM_DATASET_DIR/Path("test/"))
    


def clean_dataset():
    print_title("CLEANING DATASET")
    trainval_dir = constants.INTERIM_DATASET_DIR / Path("trainval/")
    test_dir = constants.INTERIM_DATASET_DIR / Path("test/")

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

    destination_dir = constants.PROCESSED_DATASET_DIR/Path("trainval/")
    clean(trainval_paths,destination_dir)
    
    destination_dir = constants.PROCESSED_DATASET_DIR/Path("test/")
    clean(test_paths,destination_dir)
    
    trainval_dir = constants.PROCESSED_DATASET_DIR / Path("trainval/")
    test_dir = constants.PROCESSED_DATASET_DIR / Path("test/")

    trainval_paths = glob(str(trainval_dir/Path("*")))
    test_paths = glob(str(test_dir/Path("*")))

    print("after cleaning train,test: ",len(trainval_paths),",",len(test_paths),sep="")

