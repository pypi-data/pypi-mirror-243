import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import h5py as hp
from tqdm import tqdm
from time import sleep

class FRSpy:

    def __init__(self, target, membership):
        self.membership = membership.to_numpy().astype('int32')
        self.target = target.astype('int32')

    def regions(self, h5file, key):

        POS = np.zeros((len(np.unique(self.target)), len(self.target)))
        NEG = np.zeros((len(np.unique(self.target)), len(self.target)))
        BND = np.zeros((len(np.unique(self.target)), len(self.target)))
        
        with hp.File(h5file, "r") as f:
            for instance in tqdm(f[key].keys(), desc='Computing Membership Values'): # iterating through rows
                i = int(instance[3:])
                distance = f[key][instance][:]
                for k in np.unique(self.target):
                    POS[k][i], NEG[k][i], BND[k][i] = self.process_object(i, k, distance)

        return [POS, NEG, BND]

    def process_object(self, i, k, distance):

        # lower approximation
        fuzzy_relation_i_j = distance * self.membership[i,k]
        fuzzy_implication = self.implicator(fuzzy_relation_i_j, self.membership[:,k])
        infinum = min(1, fuzzy_implication)
        inf = min(infinum, self.membership[i,k])
        
        # upper approximation
        fuzzy_relation_j_i = distance * self.membership[:,k]
        fuzzy_conjunction = self.conjunction(fuzzy_relation_j_i, self.membership[:,k])
        supremum = max(0, fuzzy_conjunction)
        sup = max(supremum, self.membership[i,k])

        return inf, 1-sup, sup-inf

    def implicator(self, a, b):
        return min(np.min(1 - a + b), 1)

    def conjunction(self, a, b):
        return max(np.max(a + b - 1), 0)

import sys
if __name__=="__main__":
  args = FRSpy(sys.argv[1], sys.argv[2]).regions(sys.argv[3], sys.argv[4])
  print("In mymodule:",args)