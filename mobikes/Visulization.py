
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
 
map = Basemap(resolution='h', llcrnrlon=113.715, llcrnrlat=22.445,
        urcrnrlon=114.7,urcrnrlat=23, projection='tmerc',lat_0=22.6,lon_0=114)
 
map.drawcoastlines()
map.fillcontinents(color='#ddaa66', lake_color='#0000ff')
map.readshapefile('./CHN_adm_shp/CHN_adm3','CHN_adm3')
plt.show()
