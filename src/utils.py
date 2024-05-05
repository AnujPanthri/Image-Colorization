import yaml
import numpy as np

class Config:
    def __init__(self,path="config.yaml"):
        with open(path,'r') as f:
            self.config = yaml.safe_load(f)
        
    def __str__(self):
        return str(self.config)
    
    def __getattr__(self, name: str):
        return self.config.get(name)
    
    # def __setattr__(self, name: str, value: any):
    #     self.config[name]=value

def is_bw(img):
    rg,gb,rb = img[:,:,0]-img[:,:,1] , img[:,:,1]-img[:,:,2] , img[:,:,0]-img[:,:,2]
    rg,gb,rb = np.abs(rg).sum(),np.abs(gb).sum(),np.abs(rb).sum()
    avg = np.mean([rg,gb,rb])
    # print(rg,gb,rb)
    
    return avg<10
    
def print_title(msg:str,n=30):
    print("="*n,msg.upper(),"="*n,sep="")

def scale_L(L):
    return L/100
def rescale_L(L):
    return L*100

def scale_AB(AB):
    return AB/128

def rescale_AB(AB):
    return AB*128
    