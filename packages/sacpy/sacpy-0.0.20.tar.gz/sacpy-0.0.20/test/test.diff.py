import sacpy as scp
import xarray as xr
import matplotlib.pyplot as plt
import sacpy.Map
import copy
# import numpy as n
# import matplotlib 

sst = scp.load_sst()['sst']

sstm = sst.mean("time").to_numpy()
# ssta = sst.drop("time")
# ssta = ssta.drop_dims("time")
# print(ssta.coords)
# print(sstm.shape)
sstm1 = scp.rewapper(sstm,sst,drop_dims="time")
# print(sstm1)

sstm1.splot()
plt.show()


# coords = sst.coords
# dim = sst.dims


# coords1 = copy.deepcopy(coords)





# newcoords = {dim[i]:coords[dim[i]] for i in range(len(dim))}
# newcoords.keys[0] = "time1"

# print(newcoords)
# print(dim)
# newc = coords

# print(type(coords))