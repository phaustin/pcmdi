import glob
from netCDF4 import Dataset
import datetime
import numpy as np
from matplotlib import pyplot as plt
from dateutil.parser import parse
import re

matchdate = re.compile('days since (.*)')

def days_to_datetime(nc_file):
    """
       input: netcdf time history variable from
              pcmdi
       output:  datetime series of days
    """
    start_day=datetime.datetime(1859,12,01)
    time_var=nc_file.variables['time']
    getgroup=matchdate.match(time_var.units)
    start_day=parse(getgroup.group(1))
    print('time varaible start day: ',time_var.units)
    print('using start date of: ',start_day)
    the_times=time_var[...]
    the_dates=[]
    for the_day in the_times:
        the_dates.append(start_day + datetime.timedelta(days=the_day))
    return the_dates

def sort_key(item):
    return item['datetimes'][0]    

def assemble_files(name_rex):
    """
         return a time-sorted  list of dicionaries containing
         the datetimes and opened nc_files for each netcdf file
    """
    filelist=glob.glob(name_rex)
    pieces=[]
    for filename in filelist:
        nc_file=Dataset(filename)
        the_times=days_to_datetime(nc_file)
        pieces.append(dict(datetimes=the_times,nc_file=nc_file))
    pieces.sort(key=sort_key)    
    for item in pieces:
        print "found segment starting at: ",item['datetimes'][0]
    return pieces


def global_average(name_rex=None,area_rex=None,nc_dir=None):
    name_rex=nc_dir + name_rex
    pieces=assemble_files(name_rex)
    area_rex=nc_dir + area_rex
    cell_file=glob.glob(area_rex)[0]
    cell_nc=Dataset(cell_file)
    areas=cell_nc.variables['areacella'][...]
    area_frac=areas/np.sum(areas.flat)

    for item in pieces:
        temps_nc=item['nc_file'].variables['ts']
        numtimes=temps_nc.shape[0]
        avg_temp=np.empty(temps_nc.shape[0],dtype=np.float)
        temp_field=np.empty(temps_nc.shape[1:],dtype=np.float)
        for index in range(numtimes):
            temp_field[...]=temps_nc[index,:,:]
            avg_temp[index]=np.sum((temp_field*area_frac).flat)
        item['ts_avg']=avg_temp
    
    all_dates=list(pieces[0]['datetimes'])
    all_temps=pieces[0]['ts_avg']
    for item in pieces[1:]:
        all_dates.extend(item['datetimes'])
        all_temps=np.concatenate([all_temps,item['ts_avg']])

    whole_years=np.int(all_temps.shape[0]/12.)
    annual_avg=all_temps[:(whole_years*12)].reshape((whole_years,-1))
    annual_avg=annual_avg.mean(axis=1)
    all_dates=np.array(all_dates)
    start_months=all_dates[:(whole_years*12)].reshape((whole_years,-1))
    start_months=start_months[:,0]
    return (start_months,annual_avg)

def find_time(name_rex,the_date=None):
    """
       find a segment containing a date
    """
    pieces=assemble_files(name_rex)
    for the_piece in pieces:
        print_vars=[the_piece['nc_file'].model_id,the_piece['nc_file'].experiment,
                    the_piece['datetimes'][0],the_piece['datetimes'][-1]]
        print "{}  {}  {}  {}".format(*print_vars) 
        "to be continued"

if __name__=="__main__":

    case_list=[]
    case_list.append(dict(name_rex='ts*ES*histor*nc',
                          area_rex="areacella_fx_*ES*.nc",
                          title="Hadley ES  historical temps"))

    case_list.append(dict(name_rex='ts*E2*histor*nc',
                          area_rex="areacella*E2*hist*.nc",
                          title="GISS E2  historical temps"))

    case_list.append(dict(name_rex='ts*GISS-E2-R_abrupt4xCO2*nc',
                          area_rex="areacella*E2*hist*.nc",
                          title="GISS E2 abrupt 4xCO2"))

    case_list.append(dict(name_rex='ts*GISS-E2-R_rcp85*nc',
                          area_rex="areacella*E2*hist*.nc",
                          title="GISS rcp8.5"))

    case_list.append(dict(name_rex='ts*ES*rcp85*nc',
                          area_rex="areacella_fx_*ES*.nc",
                          title="Hadley rcp8.5"))


    plt.close('all')
    for case_dict in case_list:
        case_dict['nc_dir']='/pip_raid/phil/gcm_e340/ncfiles/'                      
        avg_keys=['name_rex','area_rex','nc_dir']
        args={k: case_dict[k] for k in avg_keys}
        years,temps=global_average(**args)
        fig=plt.figure()
        fig.clf()
        ax1=fig.add_subplot(111)
        ax1.plot(years,temps)
        ax1.set_xlabel('years')
        ax1.set_ylabel('surface temp (K)')
        ax1.set_title(case_dict['title'])
        plt.show()


    #find_time(name_rex='ts*GISS-E2-R_abrupt4xCO2*nc')    
