from  netCDF4 import Dataset
import datetime
import numpy as np
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import Normalize
from matplotlib import cm
from matplotlib import pyplot as plt

def global_avg(temp_nc):
    """
       calculate time history of global average surface
       temperature from gisstemp file downloaded from
       http://www.esrl.noaa.gov/psd/data/gridded/data.gisstemp.html
    """
    start=datetime.datetime(1800,1,1,0,0,0)
    times=temp_nc.variables['time'][...]
    the_times=[start + datetime.timedelta(days=i) for i in times]
    lats=temp_nc.variables['lat'][...]
    lons=temp_nc.variables['lon'][...]
    temp=temp_nc.variables['air'][...]
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
    return lats,lons,the_times,the_temps
        

if __name__=="__main__":
    nc_dir='/pip_raid/phil/gcm_e340/ncfiles/'
    temps=nc_dir + 'air.2x2.250.mon.anom.comb.nc'
    temp_nc=Dataset(temps)
    lats,lons,the_times,the_temps=global_avg(temp_nc)
    fig,ax = plt.subplots(1,1)
    ax.plot(the_times,the_temps)

plt.show()
                
        
