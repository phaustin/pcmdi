from matplotlib import pyplot as plt
import numpy as np
import scipy as sp
from netCDF4 import Dataset
import netCDF4 as nc4
from mpl_toolkits.basemap import Basemap, shiftgrid, addcyclic
from matplotlib.colors import Normalize
from matplotlib import cm


plt.close('all')
filename='/media/mac2/phil/pcmdi/CanESM2/esmControl/fx/atmos/sftlf/r0i0p0/sftlf_fx_CanESM2_esmControl_r0i0p0.nc'
nc_file=Dataset(filename)
water=nc_file.variables['sftlf']
water.set_auto_maskandscale(True)
water2=water[...]
lats=nc_file.variables['lat'][...]
lons=nc_file.variables['lon'][...]

water2,lons=shiftgrid(180.,water2,lons,start=False)
water2,lons=addcyclic(water2,lons)

fig,ax = plt.subplots(1,1)
ax.cla()

cmap=cm.RdBu_r
cmap.set_over('y')
cmap.set_under('k')

vmin= 0.
vmax= 100.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)

## params=dict(projection='cyl',
##             llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180, resolution='c')
params=dict(projection='moll',lon_0=0,resolution='c')
m = Basemap(**params)
x, y = m(*np.meshgrid(lons, lats))
im=m.pcolormesh(x,y,water2,cmap=cmap,norm=the_norm,ax=ax)
cb=m.colorbar(im,extend='both',location='bottom')
ax.set_title('CanESM2 land mask')
m.drawcoastlines()
#m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(np.arange(-90.,120.,30.))
m.drawmeridians(np.arange(0.,420.,60.))
#m.drawmapboundary(fill_color='aqua')

## fig,ax = plt.subplots(1,1)
## ax.hist(water2.ravel())

plt.show()


 
