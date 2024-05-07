import tensorflow as tf
from src.utils.data_utils import rescale_AB,rescale_L
from skimage.color import lab2rgb
import numpy as np

class LogPredictionsCallback(tf.keras.callbacks.Callback):
    def __init__(self,ds,ds_name,experiment=None):
        self.ds = ds
        self.ds_name = ds_name
        self.experiment = experiment

    def on_epoch_end(self, epoch, logs=None):
        
        L_batch, _ = next(iter(self.ds))
        AB_batch = self.model.predict(L_batch,verbose=0)
        colored_batch = np.concatenate([rescale_L(L_batch),rescale_AB(AB_batch)],axis=-1)
        colored_batch = lab2rgb(colored_batch) * 255
        
        print(self.ds_name)
        print("R:",colored_batch[:,:,0].min(),colored_batch[:,:,0].max())
        print("G:",colored_batch[:,:,1].min(),colored_batch[:,:,1].max())
        print("B:",colored_batch[:,:,2].min(),colored_batch[:,:,2].max())
        
        if self.experiment:
            # log images
            for i,image in enumerate(colored_batch):
                self.experiment.log_image(image,name=f"{self.ds_name}_{i}")