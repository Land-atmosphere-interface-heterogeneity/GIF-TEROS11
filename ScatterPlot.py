# get all filename in Input/TEROS
import os
os.chdir("C:\\Users\\arenchon\\GitHub Projects\\GIF-TEROS11") # change directory if needed
Input_FN = os.listdir("Input\\TEROS") # ! filenames are in wrong order: 1,10,11,2,3, ...
Input_FN = [Input_FN[i] for i in [0,3,4,5,6,7,8,9,10,1,2]] # reorder correctly 
n = len(Input_FN)
# Load all (11 as in 11 datalogger) .csv in a list of dataframes
import pandas as pd
col_name = ['DateTime','SWC_1','Ts_1','SWC_2','Ts_2','SWC_3','Ts_3','SWC_4','Ts_4','SWC_5','Ts_5','SWC_6','Ts_6','Battery_P','Battery_V','Pressure','Log_T']
dateparse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
data = [pd.read_csv("Input\\TEROS\\"+filename,names=col_name,header=0,parse_dates=['DateTime'],date_parser=dateparse) for filename in Input_FN]
# Get all SWC data on a same continuous timestamp (11datalogger*6sensors = 66 Soil Moisture time series, but 64 in practice as 2 are empty)
Dtime = pd.date_range(start='2019-11-19 00:00:00', end='2019-12-08 00:00:00',freq='30min')
m = len(Dtime)
import numpy as np
SWC = np.empty((m,66)); SWC[:] = np.nan
nextit = range(0,5*n-1,5)
for j in range(0,n):
    for i in range(0,m):
        k = nextit[j]
        try:
            t = data[j].DateTime[data[j].DateTime == Dtime[i]].index[0]
            SWC[i][j+k] = data[j].SWC_1[t]
            SWC[i][j+1+k] = data[j].SWC_2[t]
            SWC[i][j+2+k] = data[j].SWC_3[t]
            SWC[i][j+3+k] = data[j].SWC_4[t]
            SWC[i][j+4+k] = data[j].SWC_5[t]
            SWC[i][j+5+k] = data[j].SWC_6[t]
        except:
            pass
# Outliers cleaning
np.place(SWC,SWC<0.35,np.NaN)
np.place(SWC,SWC>0.5,np.NaN)
# Load metadata file with coordinates of sensors
MD = pd.read_csv("Input\\Metadata.csv")
x = MD.x*12.5
y = MD.y*12.5
# Plotting
import matplotlib.pyplot as plt
for i in range (175,m,48):
    z = SWC[i]
    fig, ax = plt.subplots()
    im = ax.scatter(x,y,c=z, cmap=plt.cm.jet_r)
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Soil moisture')
    im.set_clim(0.35,0.48)
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title(str(Dtime[i]))
    plt.savefig('Output\\Temp\\figure'+str(i)+'.png')
plt.close('all') # close figures to save memory
import imageio
images = []
filenames = os.listdir("Output\\Temp")
for filename in filenames:
    images.append(imageio.imread("Output\\Temp\\"+filename))
imageio.mimsave('Output\\anim.gif', images)

# TO DO: add a subplot on the right, which will be animation of time series on a line where x is time and y is SWC, on same timestamp, 2nd axis y rainfall as well

# Download data from met tower at 484, store it in Input/MET TOWER folder
import wget
url = "http://www.atmos.anl.gov/ANLMET/numeric/2019/nov19met.data"
wget.download(url, 'Input\\MET TOWER\\nov19met.data')

# Load this data 








