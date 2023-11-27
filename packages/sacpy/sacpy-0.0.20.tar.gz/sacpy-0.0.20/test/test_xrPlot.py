import sacpy as scp
import sacpy.XrPlot as sxp
import sacpy.Map
import matplotlib.pyplot as plt

sst = scp.load_sst()['sst']

sst[0].splot(zero_sym=False)
plt.show()