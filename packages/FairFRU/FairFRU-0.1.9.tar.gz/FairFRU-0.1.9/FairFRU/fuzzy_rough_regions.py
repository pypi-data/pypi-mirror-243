from tables import *
import re
import pandas as pd
from .FRSpy import FRSpy
from .uncertainty import uncertainty
from .h5file_create_array import Writearray

def compute_fru(dataset, case_name, path):
  df = dataset

  # rename the column names cause they contain illegal characters and h5 cannot index columns properly
  df.columns = list(map(lambda x: re.sub('=<', 'less',x), list(df.columns)))
  df.columns = list(map(lambda x: re.sub('=>', 'more',x), list(df.columns)))
  df.columns = list(map(lambda x: re.sub('/|\(|\)|>|<|=| ', '',x), list(df.columns)))

  # fr values to fuzzy rough regions
  membership_dic = {}
  FRU = []

  target = df.iloc[:,-1]
  membership = pd.get_dummies(target)
  file_name = path+"distance_matrix_"+case_name+".h5"
  h5file = open_file(file_name, mode="w", title=case_name) # create h5 file to store distance matrix

  group = h5file.create_group("/", 'full', 'Distances after removing full') # full
  Writearray(df.iloc[:,:-1], 0.5).sim_array(h5file = h5file, group = group)

  h5file.close()

  h5file = open_file(file_name, mode="r")
  frregions = FRSpy(target, membership).regions(file_name,'full')
  membership_dic['full'] = frregions

  h5file.close()

  for s_attr in df.columns[:-1]:
    print(s_attr)

    h5file = open_file(file_name, mode="a")
    dataset = df.iloc[:,:-1].drop(s_attr, axis=1) # remove protected
    group = h5file.create_group("/", s_attr, 'Distances after removing '+s_attr)
    Writearray(dataset, 0.5).sim_array(h5file = h5file, group = group)

    h5file.close()
    h5file = open_file(file_name, mode="r")

    frregions = FRSpy(target, membership).regions(file_name,s_attr)
    membership_dic[s_attr] = frregions

    FRU.append([s_attr, uncertainty(membership_dic['full'], membership_dic[s_attr], 0)])
    h5file.close()

  return FRU, membership_dic

import sys
if __name__=="__main__":
  args = compute_fru(sys.argv)
  print("In mymodule:",args)