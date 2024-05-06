import tensorflow as tf
from src.utils.data_utils import scale_L,scale_AB,rescale_AB,rescale_L
from src.utils.config_loader import config,constants
from pathlib import Path
from glob import glob
import sklearn.model_selection
from skimage.color import rgb2lab, lab2rgb

def get_datasets():
    trainval_dir = constants.PROCESSED_DATASET_DIR / Path("trainval/")
    test_dir = constants.PROCESSED_DATASET_DIR / Path("test/")

    trainval_paths = glob(str(trainval_dir/Path("*")))
    test_paths = glob(str(test_dir/Path("*")))

    len(trainval_paths),len(test_paths)



    train_paths,val_paths = sklearn.model_selection.train_test_split(trainval_paths,
                                                                    train_size=0.8,
                                                                    random_state=324)
    
    print("train|val|test:",len(train_paths),"|",len(val_paths),"|",len(test_paths))
    
    train_ds = get_tf_ds(train_paths,bs=config.batch_size,shuffle=config.shuffle)
    val_ds = get_tf_ds(val_paths,bs=config.batch_size,shuffle=False,is_val=True)
    test_ds = get_tf_ds(test_paths,bs=config.batch_size,shuffle=False,is_val=True)
    
    return train_ds,val_ds,test_ds


def tf_RGB_TO_LAB(image):
    def f(image):
        image = rgb2lab(image)
        return image
    lab = tf.numpy_function(f,[image],tf.float32)
    lab.set_shape(image.shape)
    return lab


# load the image in lab space and split the l and ab channels
def load_img(img_path):
    img_bytes = tf.io.read_file(img_path)
    image = tf.image.decode_image(img_bytes,3,expand_animations=False)
    image = tf.image.resize(image,[config.image_size,config.image_size])
    image = image / 255.0
    image = tf_RGB_TO_LAB(image)

    L,AB = image[:,:,0:1],image[:,:,1:]
    L,AB = scale_L(L),scale_AB(AB)
    return L,AB
    
def get_tf_ds(image_paths,bs=8,shuffle=False,is_val=False):
    ds = tf.data.Dataset.from_tensor_slices(image_paths)
    if shuffle:   ds = ds.shuffle(len(image_paths))
    ds = ds.map(load_img,num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.batch(bs,num_parallel_calls=tf.data.AUTOTUNE,drop_remainder=not is_val)
    
    return ds

