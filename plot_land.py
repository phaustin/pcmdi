from mpl_toolkits.basemap import Basemap,shiftgrid, addcyclic
from matplotlib.colors import Normalize
from matplotlib import cm
from matplotlib import pyplot as plt
from netCDF4 import Dataset
import  numpy as np

def doplot(nc_file):
    lons=nc_file.variables['lon'][...]
    lats=nc_file.variables['lat'][...]
    vals=nc_file.variables['sftlf'][...]
    vals,lons=shiftgrid(180.,vals,lons,start=True)
    vals,lons=addcyclic(vals,lons)
    fig,ax = plt.subplots(1,1)
    ax.cla()
    cmap=cm.RdBu_r
    cmap.set_over('y')
    cmap.set_under('k')
    vmin= 0.
    vmax= 1.
    the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
    params=dict(projection='moll',lon_0= -100,resolution='c')
    m = Basemap(**params)
    x, y = m(*np.meshgrid(lons, lats))
    im=m.pcolormesh(x,y,vals,cmap=cmap,norm=the_norm,ax=ax)
    cb=m.colorbar(im,extend='both',location='bottom')
    ## corner_lats=[-10.,-10.,+15.,+15.,-10.]
    ## corner_lons=[85.,160.,160.,85.,85.]
    ## x,y=m(corner_lons,corner_lats)
    ## m.plot(x,y,lw=5.,ax=ax)
    m.drawcoastlines()
    #m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    m.drawparallels(np.arange(-35.,35.,5.))
    m.drawmeridians(np.arange(80.,160.,5.))
    #m.drawmapboundary(fill_color='aqua')
    ax.set_title('gridcell areas in 1000 km^2')
    ## fig,ax = plt.subplots(1,1)
    ## ax.hist(wap_850.ravel())
    return fig,ax


land='sftlf_fx_GISS-E2-R_historical_r0i0p0.nc'
land_nc=Dataset(land)
plt.close('all')
fig,ax=doplot(land_nc)
plt.show()
## fig,ax = plt.subplots(1,1)
## ax.plot(the_times,the_temps)
