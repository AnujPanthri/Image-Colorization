import os,sys;sys.path.append(os.getcwd())
from src.data.load_dataset import get_ds,get_datasets
from src import config
from src.utils import *
import matplotlib.pyplot as plt
import cv2
import math

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


def visualize_dataset():
    train_ds,val_ds,test_ds = get_datasets()    
    L_batch,AB_batch = next(iter(train_ds))
    L_batch,AB_batch = L_batch.numpy(), AB_batch.numpy()
    see_batch(L_batch,
              AB_batch,
              title="training dataset")
    
    L_batch,AB_batch = next(iter(val_ds))
    L_batch,AB_batch = L_batch.numpy(), AB_batch.numpy()
    see_batch(L_batch,
              AB_batch,
              title="validation dataset")
    
    L_batch,AB_batch = next(iter(test_ds))
    L_batch,AB_batch = L_batch.numpy(), AB_batch.numpy()
    see_batch(L_batch,
              AB_batch,
              title="testing dataset")
    

