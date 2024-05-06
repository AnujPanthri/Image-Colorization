from src.simple_regression_colorization.model.base_model_interface import BaseModel
from src.simple_regression_colorization.model.dataloaders import get_datasets
from src.utils.config_loader import config
from src.utils.data_utils import scale_L,scale_AB,rescale_AB,rescale_L,see_batch
from skimage.color import lab2rgb
import tensorflow as tf
from tensorflow.keras import layers,Model as keras_Model,Sequential
import numpy as np

def down(filters,kernel_size,apply_batch_normalization=True):
    down = Sequential()
    down.add(layers.Conv2D(filters,kernel_size,padding="same",strides=2))
    if apply_batch_normalization:
        down.add(layers.BatchNormalization())
    down.add(layers.LeakyReLU())
    return down

def up(filters,kernel_size,dropout=False):
    upsample = Sequential()
    upsample.add(layers.Conv2DTranspose(filters,kernel_size,padding="same",strides=2))
    if dropout:
        upsample.add(layers.Dropout(dropout))
    upsample.add(layers.LeakyReLU())
    return upsample

class Model(BaseModel):
    
    def __init__(self,path=None):
        # make model architecture
        # load weights (optional)
        # create dataset loaders
        # train
        # predict
        self.init_model()
        self.load_weights(path)
        

    def init_model(self):
        x = layers.Input([config.image_size,config.image_size,1])
        d1 = down(128,(3,3),False)(x)
        d2 = down(128,(3,3),False)(d1)
        d3 = down(256,(3,3),True)(d2)
        d4 = down(512,(3,3),True)(d3)
        d5 = down(512,(3,3),True)(d4)
        
        u1 = up(512,(3,3))(d5)
        u1 = layers.concatenate([u1,d4])
        u2 = up(256,(3,3))(u1)
        u2 = layers.concatenate([u2,d3])
        u3 = up(128,(3,3))(u2)
        u3 = layers.concatenate([u3,d2])
        u4 = up(128,(3,3))(u3)
        u4 = layers.concatenate([u4,d1])
        u5 = up(64,(3,3))(u4)
        u5 = layers.concatenate([u5,x])
        
        y = layers.Conv2D(2,(2,2),strides = 1, padding = 'same',activation="tanh")(u5)

        self.model = keras_Model(x,y,name="UNet")


    def load_weights(self,path=None):
        if path:
            self.model.load_weights(path)

    def prepare_data(self):
        self.train_ds,self.val_ds,self.test_ds = get_datasets()
        
    def train(self):

        self.prepare_data()
        self.model.compile(optimizer="adam",loss="mse",metrics=["mae","acc"])
        self.history = self.model.fit(self.train_ds,
                                      validation_data=self.val_ds,
                                      epochs=config.epochs)

    def save(self,model_path):
        self.model.save_weights(model_path)

    def predict(self,L_batch):
        L_batch = scale_L(L_batch)
        AB_batch = self.model.predict(L_batch,verbose=0)
        return rescale_AB(AB_batch)

    def evaluate(self):
        train_metrics = self.model.evaluate(self.train_ds)
        val_metrics = self.model.evaluate(self.val_ds)
        test_metrics = self.model.evaluate(self.test_ds)

        return {
            "train": train_metrics,
            "val": val_metrics,
            "test": test_metrics,
        }

    def predict_colors(self,L_batch):
        AB_batch = self.predict(L_batch)
        colored_batch = np.concatenate([L_batch,rescale_AB(AB_batch)],axis=-1)
        colored_batch = lab2rgb(colored_batch) * 255
        return colored_batch

    def show_results(self):
        self.prepare_data()
        
        L_batch,AB_batch = next(iter(self.train_ds))
        L_batch = L_batch.numpy()
        AB_pred = self.model.predict(L_batch,verbose=0)
        see_batch(L_batch,AB_pred,title="Train dataset Results")
        
        L_batch,AB_batch = next(iter(self.val_ds))
        L_batch = L_batch.numpy()
        AB_pred = self.model.predict(L_batch,verbose=0)
        see_batch(L_batch,AB_pred,title="Val dataset Results")
        
        L_batch,AB_batch = next(iter(self.test_ds))
        L_batch = L_batch.numpy()
        AB_pred = self.model.predict(L_batch,verbose=0)
        see_batch(L_batch,AB_pred,title="Test dataset Results")
        
