import tensorflow as tf
from tensorflow.keras import layers,Model as keras_Model,Sequential

def down_block(filters,kernel_size,apply_batch_normalization=True):
    down = Sequential()
    down.add(layers.Conv2D(filters,kernel_size,padding="same",strides=2))
    if apply_batch_normalization:
        down.add(layers.BatchNormalization())
    down.add(layers.LeakyReLU())
    return down

def up_block(filters,kernel_size,dropout=False):
    upsample = Sequential()
    upsample.add(layers.Conv2DTranspose(filters,kernel_size,padding="same",strides=2))
    if dropout:
        upsample.add(layers.Dropout(dropout))
    upsample.add(layers.LeakyReLU())
    return upsample
