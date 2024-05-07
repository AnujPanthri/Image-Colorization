from src.simple_regression_colorization.model.base_model_interface import BaseModel
from src.utils.config_loader import config
from src.simple_regression_colorization.model.model_utils import up_block,down_block
import tensorflow as tf
from tensorflow.keras import layers,Model as keras_Model,Sequential


class Model(BaseModel):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def init_model(self):
        x = layers.Input([config.image_size,config.image_size,1])
        d1 = down_block(128,(3,3),False)(x)
        d2 = down_block(128,(3,3),False)(d1)
        d3 = down_block(256,(3,3),True)(d2)
        d4 = down_block(512,(3,3),True)(d3)
        d5 = down_block(512,(3,3),True)(d4)
        
        u1 = up_block(512,(3,3))(d5)
        u1 = layers.concatenate([u1,d4])
        u2 = up_block(256,(3,3))(u1)
        u2 = layers.concatenate([u2,d3])
        u3 = up_block(128,(3,3))(u2)
        u3 = layers.concatenate([u3,d2])
        u4 = up_block(128,(3,3))(u3)
        u4 = layers.concatenate([u4,d1])
        u5 = up_block(64,(3,3))(u4)
        u5 = layers.concatenate([u5,x])
        
        y = layers.Conv2D(2,(2,2),strides = 1, padding = 'same',activation="tanh")(u5)

        self.model = keras_Model(x,y,name="UNet")