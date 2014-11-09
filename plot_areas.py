"""
look at the average omega in the warm pool box as a monthly time series

"""

from matplotlib import pyplot as plt
import numpy as np
import scipy as sp
from netCDF4 import Dataset
import netCDF4 as nc4
from mpl_toolkits.basemap import Basemap, shiftgrid, addcyclic
from matplotlib.colors import Normalize
from matplotlib import cm
import datetime
from constants import warm_pool as wp
import collections
from util import find_index
import glob


plt.close('all')
area_file=glob.glob("areacella_fx_HadGEM2*nc")[0]
mask_file=glob.glob("sftlf_fx_HadGEM2*nc")[0]
#area_file='/Volumes/mac2/phil/pcmdi/CanESM2/esmControl/fx/atmos/areacella/r0i0p0/areacella_fx_CanESM2_esmControl_r0i0p0.nc'
#mask_file='/Volumes/mac2/phil/pcmdi/CanESM2/esmControl/fx/atmos/sftlf/r0i0p0/sftlf_fx_CanESM2_esmControl_r0i0p0.nc'

nc_area=Dataset(area_file)
lats=nc_area.variables['lat'][...]
lons=nc_area.variables['lon'][...]

lat_bounds=find_index(lats,[wp.ll.lat,wp.ur.lat])
lat_bounds[1]+=1
lon_bounds=find_index(lons,[wp.ll.lon,wp.ur.lon])
lon_bounds[1]+=1

lat_bounds=(0,None)
lon_bounds=(0,None)

lat_bounds=slice(*lat_bounds)
lon_bounds=slice(*lon_bounds)

areas=nc_area.variables['areacella'][lat_bounds,lon_bounds]
lats=lats[lat_bounds]
lons=lons[lon_bounds]




plt.close('all')
fig,ax = plt.subplots(1,1)
ax.cla()

cmap=cm.RdBu_r
cmap.set_over('y')
cmap.set_under('k')

#convert from m^2 1000 km^2
areas=areas*1.e-9
vmin= 0.
vmax= 29.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
params=dict(projection='ortho',
            lat_0=0.,lon_0=120., resolution='c')
## params=dict(projection='merc',
##             llcrnrlon=80,llcrnrlat=-35.,urcrnrlon=160,urcrnrlat=35.,
##             resolution='c',lat_0=0,lon_0=120.,lat_ts=0.)
params=dict(projection='moll',lon_0= 100,resolution='c')
m = Basemap(**params)
x, y = m(*np.meshgrid(lons, lats))
im=m.pcolormesh(x,y,areas,cmap=cmap,norm=the_norm,ax=ax)
cb=m.colorbar(im,extend='both',location='bottom')
corner_lats=[-10.,-10.,+15.,+15.,-10.]
corner_lons=[85.,160.,160.,85.,85.]
x,y=m(corner_lons,corner_lats)
m.plot(x,y,lw=5.,ax=ax)
m.drawcoastlines()
#m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(np.arange(-35.,35.,5.))
m.drawmeridians(np.arange(80.,160.,5.))
#m.drawmapboundary(fill_color='aqua')
ax.set_title('gridcell areas in 1000 km^2')
## fig,ax = plt.subplots(1,1)
## ax.hist(wap_850.ravel())
plt.show()


 


 
