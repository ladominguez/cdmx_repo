import pandas as pd
import numpy as np
from glob import glob
from datetime import datetime
from matplotlib import pyplot as plt

names = ['No', 'Date', 'Time', 'latitude', 'longitude', 'Depth', 'Mag', 'CC', 'MAD', 'Reference']
dtypes = {'No': int, 'Date': str, 'Time': str, 'latitude': float, 'longitude': float, 'Depth': float, 'Mag': float,
          'CC': float, 'MAD': float, 'Reference': str}

colors = ['red', 'blue', 'orange', 'teal', 'black', 'green', 'purple']

def get_color(colors=colors):
    return np.roll(colors, 1)
limit = 9.5
if __name__ ==  '__main__':

    input_files = glob('DetectedFinal_All_*.dat')
    
    fig, ax = plt.subplots(len(input_files), 1, figsize=(14, 8), sharex=True)

    for k, file in enumerate(input_files):
        catalog =  pd.read_csv(file, sep='\s+', header = 0, names=names, dtype=dtypes)
        catalog['Date'] = catalog['Date'].str.cat(catalog['Time'], sep=' ')
        catalog['Date'] = pd.to_datetime(catalog['Date'], format='%Y/%m/%d %H:%M:%S.%f')
        catalog = catalog.drop(columns=['Time'])

        config = file.split('_')
        t0 = datetime.strptime(config[2], '%Y%m%d')
        t1 = datetime.strptime(config[3], '%Y%m%d')
        dlat = float(config[11])*111.11*1000
        dlon = float(config[12])*111.11*1000
        ddep = float(config[13])*1000

        
        Dlat = float(config[15])*111.11*1000
        Dlon = float(config[16])*111.11*1000
        Ddep = float(config[17])*1000

        DT = float(config[19])

        dt_filter = catalog[catalog['CC'] < 0.95]
        dt_filter2 = dt_filter[dt_filter['MAD'] >= limit]
        colors=get_color(colors)

        ax[k].plot(dt_filter['Date'], dt_filter['MAD'], 'o', color = colors[0], label = 'No. eq = ' + str(len(catalog))
                   + " detection (MAD>9.5)= " + str(len(dt_filter2)) )
        #ax[k].plot(catalog['Date'], catalog['MAD'], 'o', color = colors[0], label = 'Catalog - 0' + str(k+1) )
        ax[k].set_ylabel('MAD')
        ax[k].legend()
        ax[k].axhline(y=limit, color='r', linestyle='--')
        ax[k].axhline(y=10,    color='r', linestyle='--')
        ax[k].set_title(file)
        ax[k].grid()
        ax[k].set_ylim(9, 11)
        
        print("=========================================================================================================================")
        print(file)
        print('Catalog - 0' + str(k+1))
        print('Number of events: ', len(catalog), 'Number of filtered events: ', len(dt_filter), 'Number of filtered events2: ', len(dt_filter2))
        print('Mean MAD: ', np.mean(dt_filter['MAD']), 'STD MAD: ', np.std(dt_filter['MAD']))
        print('Max MAD: ', catalog['MAD'].max())
        print('Mean CC: ', np.mean(dt_filter['CC']), 'STD CC: ', np.std(dt_filter['CC']))
        print("dlat: ", dlat, " dlon: ", dlon, " ddep: ", ddep, " Dlat: ", Dlat, " Dlon: ", Dlon, " Ddep: ", Ddep, " Win: ", DT)


    print('Saving figure results.png')
    fig.savefig('results.png')
        
