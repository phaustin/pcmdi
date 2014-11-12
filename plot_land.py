from mpl_toolkits.basemap import Basemap,shiftgrid, addcyclic
from matplotlib.colors import Normalize
from matplotlib import cm
from matplotlib import pyplot as plt
from netCDF4 import Dataset
import  numpy as np

def doplot(nc_file=None,varname=None,vmin=None,vmax=None,
           title=None):
    lons=nc_file.variables['lon'][...]
    lats=nc_file.variables['lat'][...]
    vals=nc_file.variables[varname]
    vals.set_auto_maskandscale(True)
    vals=vals[...]
    vals,lons=shiftgrid(180.,vals,lons,start=False)
    vals,lons=addcyclic(vals,lons)
    fig,ax = plt.subplots(1,1)
    ax.cla()
    cmap=cm.RdBu_r
    cmap.set_over('y')
    cmap.set_under('k')
    the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
    params=dict(projection='moll',lon_0= 0,resolution='c')
    m = Basemap(**params)
    x, y = m(*np.meshgrid(lons, lats))
    im=m.pcolormesh(x,y,vals,cmap=cmap,norm=the_norm,ax=ax)
    cb=m.colorbar(im,extend='both',location='bottom')
    m.drawcoastlines()
    m.drawparallels(np.arange(-90.,120.,30.))
    m.drawmeridians(np.arange(0.,420.,60.))
    ax.set_title(title)
    return fig,m,ax,vals,lons

if __name__== "__main__":
    nc_dir='/pip_raid/phil/gcm_e340/ncfiles/'
    land=nc_dir + 'sftlf_fx_GISS-E2-R_historical_r0i0p0.nc'
    land_nc=Dataset(land)
    oro=nc_dir + 'orog_fx_GISS-E2-R_historical_r0i0p0.nc'
    orog_nc=Dataset(oro)
    plt.close('all')
    vals=dict(nc_file=land_nc,varname='sftlf',vmin=0.,vmax=100.,
              title='land fraction (%)')
    fig1,m1,ax1,sftlf1,lons1=doplot(**vals)

    vals=dict(nc_file=orog_nc,varname='orog',vmin=0.,vmax=6000.,
              title='surface elevation (m)')
    fig,m,ax,vals,lons=doplot(**vals)
    plt.show()

