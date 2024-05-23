import numpy as np
from abc import ABC, abstractmethod
from src.simple_regression_colorization.model.dataloaders import get_datasets
from src.utils.data_utils import scale_L,scale_AB,rescale_AB,rescale_L,see_batch
from src.utils.config_loader import config
from skimage.color import lab2rgb
from src.simple_regression_colorization.model.callbacks import LogPredictionsCallback

# BaseModel Abstract class
# all the models within this sub_task must inherit this class

class BaseModel(ABC):
    def __init__(self,path=None,experiment=None):
        self.init_model()
        self.load_weights(path)
        self.experiment = experiment
    
    def load_weights(self,path=None):
        if path:
            self.model.load_weights(path)

    def prepare_data(self):
        self.train_ds,self.val_ds,self.test_ds = get_datasets()

    def train(self):

        self.prepare_data()
        self.model.compile(optimizer="adam",loss="mse",metrics=["mae","acc"])
        
        callbacks = [
            LogPredictionsCallback(self.train_ds,"train_ds",self.experiment),
            LogPredictionsCallback(self.val_ds,"val_ds",self.experiment),
        ]

        self.history = self.model.fit(self.train_ds,
                                      validation_data=self.val_ds,
                                      callbacks=callbacks,
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
        colored_batch = np.concatenate([L_batch,AB_batch],axis=-1)
        colored_batch = lab2rgb(colored_batch) * 255
        return colored_batch.astype("uint8")

    def show_results(self):
        self.prepare_data()
        
        L_batch,AB_batch = next(iter(self.train_ds))
        L_batch = L_batch.numpy()
        AB_pred = self.model.predict(L_batch,verbose=0)
        see_batch(L_batch,
                  AB_pred,
                  title="Train dataset Results",
                  save = True,
                  label = "train",
                  )
        
        L_batch,AB_batch = next(iter(self.val_ds))
        L_batch = L_batch.numpy()
        AB_pred = self.model.predict(L_batch,verbose=0)
        see_batch(L_batch,
                  AB_pred,
                  title="Val dataset Results",
                  save = True,
                  label = "val",
                  )
        
        L_batch,AB_batch = next(iter(self.test_ds))
        L_batch = L_batch.numpy()
        AB_pred = self.model.predict(L_batch,verbose=0)
        see_batch(L_batch,
                  AB_pred,
                  title="Test dataset Results",
                  save = True,
                  label = "test",
                  )
        

    @abstractmethod
    def init_model(self):
        pass
        
  