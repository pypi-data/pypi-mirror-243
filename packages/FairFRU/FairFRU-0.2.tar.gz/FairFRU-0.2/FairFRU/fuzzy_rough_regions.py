from tables import *
import re
import pandas as pd
from .FRSpy import FRSpy
from .h5file_create_array import Writearray
import h5py

def compute_fru(dataset, case_name, path):
  df = dataset

  # rename the column names cause they contain illegal characters and h5 cannot index columns properly
  df.columns = list(map(lambda x: re.sub('=<', 'less',x), list(df.columns)))
  df.columns = list(map(lambda x: re.sub('=>', 'more',x), list(df.columns)))
  df.columns = list(map(lambda x: re.sub('/|\(|\)|>|<|=| ', '',x), list(df.columns)))

  # fr values to fuzzy rough regions

  target = df.iloc[:,-1]
  membership = pd.get_dummies(target)
  file_name = path+"distance_matrix_"+case_name+".h5"
  h5file = open_file(file_name, mode="w", title=case_name) # create h5 file to store distance matrix

  group = h5file.create_group("/", 'full', 'Distances after removing full') # full
  Writearray(df.iloc[:,:-1], 0.5).sim_array(h5file = h5file, group = group)

  h5file.close()

  h5file = open_file(file_name, mode="r")
  frregions = FRSpy(target, membership).regions(file_name,'full')

  with open('full_mem.pickle', 'wb') as handle:
    pickle.dump(frregions, handle, protocol=pickle.HIGHEST_PROTOCOL)
  h5file.close()

  h5file = h5py.File(file_name, mode="a")
  del h5file['full']
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
    with open(s_attr+'_mem.pickle', 'wb') as handle:
      pickle.dump(frregions, handle, protocol=pickle.HIGHEST_PROTOCOL)
    h5file.close()

    h5file = h5py.File(file_name, mode="a")
    del h5file[s_attr]
    h5file.close()

import sys
if __name__=="__main__":
  args = compute_fru(sys.argv)
  print("In mymodule:",args)