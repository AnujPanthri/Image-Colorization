from src.utils.config_loader import constants
from huggingface_hub import snapshot_download
from zipfile import ZipFile
import numpy as np
import os,shutil
import matplotlib.pyplot as plt
import cv2
import math


def download_hf_dataset(repo_id,allow_patterns=None):
    """Used to download dataset from any public hugging face dataset"""
    snapshot_download(repo_id=repo_id,
                    repo_type="dataset",
                    local_dir=constants.RAW_DATASET_DIR,
                    allow_patterns=allow_patterns)


def download_personal_hf_dataset(name):
    """Used to download dataset from a specific hugging face dataset"""
    download_hf_dataset(repo_id="Anuj-Panthri/Image-Colorization-Datasets",
                        allow_patterns=f"{name}/*")


def unzip_file(file_path,destination_dir):
    """unzips file to destination_dir"""
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.makedirs(destination_dir)
    with ZipFile(file_path,"r") as zip:
        zip.extractall(destination_dir)

def is_bw(img:np.ndarray):
    """checks if RGB image is black and white"""
    rg,gb,rb = img[:,:,0]-img[:,:,1] , img[:,:,1]-img[:,:,2] , img[:,:,0]-img[:,:,2]
    rg,gb,rb = np.abs(rg).sum(),np.abs(gb).sum(),np.abs(rb).sum()
    avg = np.mean([rg,gb,rb])
    
    return avg<10


def print_title(msg:str,max_chars=105):
    n = (max_chars-len(msg))//2
    print("="*n,msg.upper(),"="*n,sep="")

def scale_L(L):
    return L/100

def rescale_L(L):
    return L*100

def scale_AB(AB):
    return AB/128

def rescale_AB(AB):
    return AB*128
    


def show_images_from_paths(image_paths:list[str],image_size=64,cols=4,row_size=5,col_size=5,show_BW=False,title=None):
    n = len(image_paths)
    rows = math.ceil(n/cols)
    fig = plt.figure(figsize=(col_size*cols,row_size*rows))
    if title:
        plt.title(title)
    plt.axis("off")

    for i in range(n):
        fig.add_subplot(rows,cols,i+1)
        
        img = cv2.imread(image_paths[i])[:,:,::-1]
        img = cv2.resize(img,[image_size,image_size])

        if show_BW:
            BW = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
            BW = np.tile(BW,(1,1,3))
            img = np.concatenate([BW,img],axis=1)
        plt.imshow(img.astype("uint8"))
    plt.show()


def see_batch(L_batch,AB_batch,show_L=False,cols=4,row_size=5,col_size=5,title=None):
    n = L_batch.shape[0]
    rows = math.ceil(n/cols)
    fig = plt.figure(figsize=(col_size*cols,row_size*rows))
    if title:
        plt.title(title)
    plt.axis("off")
    
    for i in range(n):
        fig.add_subplot(rows,cols,i+1)
        L,AB = L_batch[i],AB_batch[i]
        L,AB = rescale_L(L), rescale_AB(AB)
#         print(L.shape,AB.shape)
        img = np.concatenate([L,AB],axis=-1)
        img = cv2.cvtColor(img,cv2.COLOR_LAB2RGB)*255
#         print(img.min(),img.max())
        if show_L:
            L = np.tile(L,(1,1,3))/100*255
            img = np.concatenate([L,img],axis=1)
        plt.imshow(img.astype("uint8"))
    plt.show()
