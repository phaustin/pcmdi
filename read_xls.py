from openpyxl import load_workbook
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as md

def sheet_dataframe(sheet):
    region=sheet['A6':'I245']
    num_rows=len(region)
    num_cols=len(region[0])
    the_rows=[]
    for row in range(num_rows):
        col_list=[]
        for col in range(num_cols):
            if col==0:
                value=datetime.datetime(region[row][col].value,1,1)
            else:
                value=region[row][col].value
            col_list.append(value)
        the_rows.append(col_list)
    line=sheet['A5':'I5']        
    header=[item.value for item in line[0]]
    header=[item.replace(' ','_') for item in header]
    header=[item.lower() for item in header]
    df=pd.DataFrame.from_records(the_rows,columns=header)
    return df

name='Project7_model.xlsx'
wb = load_workbook(name,data_only=True)
B1_sh,A2_sh=wb.get_sheet_names()
sheet=wb[A2_sh]
df_a2=sheet_dataframe(sheet)
sheet=wb[B1_sh]
df_b1=sheet_dataframe(sheet)

plt.close('all')
fig=plt.figure(1)
ax1=fig.add_subplot(111)
xfmt=md.DateFormatter('%Y')
the_dates=[item.to_datetime() for item in df_a2.year]
ax1.xaxis.set_major_formatter(xfmt)
ax1.plot(the_dates,df_a2.gasses,label='gasses')
ax1.plot(the_dates,df_a2.aerosols,label='aerosols')
ax1.plot(the_dates,df_a2.volcanic,label='volcanic')
ax1.plot(the_dates,df_a2.solar,label='solar')
ax1.legend(loc='best')
fig.tight_layout()
fig.canvas.draw()

fig=plt.figure(2)
ax1=fig.add_subplot(111)
xfmt=md.DateFormatter('%Y')
the_dates=[item.to_datetime() for item in df_b1.year]
ax1.xaxis.set_major_formatter(xfmt)
ax1.plot(the_dates,df_b1.gasses,label='gasses')
ax1.plot(the_dates,df_b1.aerosols,label='aerosols')
ax1.plot(the_dates,df_b1.volcanic,label='volcanic')
ax1.plot(the_dates,df_b1.solar,label='solar')
ax1.legend(loc='best')
fig.tight_layout()
fig.canvas.draw()

plt.show()


        

