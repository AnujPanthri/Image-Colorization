from src.utils.data_utils import show_images_from_paths
from src.utils.config_loader import constants,config
from glob import glob
import numpy as np

# the data is at constants.PROCESSED_DATASET_DIR/trainval
#                constants.PROCESSED_DATASET_DIR/test

def visualize():
    n = 16
    image_paths = glob(f"{constants.PROCESSED_DATASET_DIR}/trainval/*")
    choosen_paths = np.random.choice(image_paths,n,replace=False)
    show_images_from_paths(choosen_paths,
                           title="sample of train_val dataset",
                           image_size=config.image_size,
                           save=True,
                           label="trainval",
                           )

    image_paths = glob(f"{constants.PROCESSED_DATASET_DIR}/test/*")
    choosen_paths = np.random.choice(image_paths,n,replace=False)
    show_images_from_paths(choosen_paths,
                           title="sample of test dataset",
                           image_size=config.image_size,
                           save=True,
                           label="test",
                           )