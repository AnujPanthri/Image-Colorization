from src.simple_regression_colorization.model.base_model_interface import BaseModel
from src.simple_regression_colorization.model.dataloaders import get_datasets

class Model(BaseModel):
    
    def __init__(self):
        # make model architecture
        # load weights (optional)
        # create dataset loaders
        # train
        # predict
        self.init_model()
        self.load_weights()
        self.prepare_data()
        

    def init_model(self):
        pass

    def load_weights(self,path=None):
        pass

    def prepare_data(self):
        self.train_ds,self.val_ds,self.test_ds = get_datasets()
        
    def train(self):
        pass
        
    def predict(self,inputs):
        pass
