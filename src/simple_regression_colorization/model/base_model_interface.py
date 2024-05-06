import numpy as np
from abc import ABC, abstractmethod

# BaseModel Abstract class
# all the models within this sub_task must inherit this class

class BaseModel(ABC):
    @abstractmethod
    def train(self):
        pass
        
    @abstractmethod        
    def predict(self,inputs):
        pass
