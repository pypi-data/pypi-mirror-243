import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import sacpy as scp
import sacpy.Map
import copy
# a = np.arange(10)
# b = a.copy()

# a1 = xr.DataArray(a)
# a1.copy()

sst = scp.load_sst()['sst']
coords = copy.deepcopy(sst.coords)

del coords['time']
print(coords)
# print(sst)
print(sst.coords)
# print(sst.coords.drop('time'))
# sst.splot()
# plt.show()
# ssta = scp.get_anom(sst,method=1)
# Nino34 = ssta.loc[:,-5:5,190:240].mean(axis=(1,2))
# linreg = scp.LinReg(Nino34,ssta)

# p = linreg.p_value
# sl = linreg.slope
# sl1 = sl.to_numpy()
# linreg.mask(threshold=0.00000000000001)

# linreg.slope1.plot()

# plt.show()
