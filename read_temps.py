from  netCDF4 import Dataset
import datetime
import numpy as np
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import Normalize
from matplotlib import cm
from matplotlib import pyplot as plt

start=datetime.datetime(1800,1,1,0,0,0)
the_file='air.2x2.250.mon.anom.comb.nc'
out=Dataset(the_file)
times=out.variables['time'][...]
the_times=[start + datetime.timedelta(days=i) for i in times]

lats=out.variables['lat'][...]
lons=out.variables['lon'][...]
temp=out.variables['air'][...]

areas=np.empty([lats.shape[0],lons.shape[0]],dtype=np.float)

R2=6371.**2.
deg2rad=np.pi/180.
dlat=2.*deg2rad
dlon=2.*deg2rad
for row,the_lat in enumerate(lats):
    for col,the_lon in enumerate(lons):
        abs_lat=np.abs(the_lat)
        co_lat=(90. - abs_lat)*deg2rad
        areas[row,col]=R2*np.sin(co_lat)*dlat*dlon

tot_area=np.sum(areas.flat)
num_times=temp.shape[0]
the_temps=np.empty([num_times],dtype=np.float)
for the_time in range(num_times):
    product=(temp[the_time,:,:]*areas).ravel()
    avg_temp=np.sum(product)/tot_area
    the_temps[the_time]=avg_temp

        
                
plt.close('all')
fig,ax = plt.subplots(1,1)
ax.cla()
cmap=cm.RdBu_r
cmap.set_over('y')
cmap.set_under('k')
areas=areas*1.e-3  #1000 km^2
vmin= 0.
vmax= 50.
the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
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

fig,ax = plt.subplots(1,1)
ax.plot(the_times,the_temps)


plt.show()
                
        
