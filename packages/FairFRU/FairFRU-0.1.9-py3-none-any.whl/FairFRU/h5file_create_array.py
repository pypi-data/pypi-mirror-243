import numpy as np
from tables import *
from tqdm import tqdm
from time import sleep

class Writearray:

    def __init__(self, df, alpha):
        
        self.numeric = [False if df[col].dtype == 'object' else True for col in df]
        self.nominal = [True if df[col].dtype == 'object' else False for col in df]

        num = df.loc[:,self.numeric]
        scaled=np.subtract(num,np.min(num,axis=0))/np.subtract(np.max(num,axis=0),np.min(num,axis=0))
        df[df.columns[self.numeric]] = scaled.round(3).astype('float32')

        self.df = df.values
        self.alpha = alpha

    def sim_array(self, h5file, group):
       for instance in tqdm(range(0,len(self.df)), desc='Building similarity matrix'):
          sim = self.similarity(instance)
          h5file.create_array(group, 'col'+str(instance), sim, 'Distance instance '+str(instance))

    def similarity(self, i):
        d = np.sum(np.abs(np.subtract(self.df[i][self.numeric], self.df[:,self.numeric])), axis=1) + np.sum(self.df[i][self.nominal] != self.df[:,self.nominal],axis=1)
        return np.exp(-self.alpha * d.astype('float32'))
    
import sys
if __name__=="__main__":
  args = Writearray(sys.argv).sim_array(sys.argv)
  print("In mymodule:",args)