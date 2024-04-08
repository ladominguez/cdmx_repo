import pandas as pd
import numpy as np
from glob import glob
from datetime import datetime
from matplotlib import pyplot as plt

names = ['No', 'Date', 'Time', 'latitude', 'longitude', 'Depth', 'Mag', 'CC', 'MAD', 'Reference']
dtypes = {'No': int, 'Date': str, 'Time': str, 'latitude': float, 'longitude': float, 'Depth': float, 'Mag': float,
          'CC': float, 'MAD': float, 'Reference': str}

if __name__ ==  '__main__':

    input_files = glob('DetectedFinal_All_*.dat')

    for file in input_files:
        catalog =  pd.read_csv(file, delim_whitespace=True, header = 1, names=names, dtype=dtypes)
        catalog['Date'] = catalog['Date'].str.cat(catalog['Time'], sep=' ')
        catalog['Date'] = pd.to_datetime(catalog['Date'], format='%Y/%m/%d %H:%M:%S.%f')
        catalog = catalog.drop(columns=['Time'])

        config = file.split('_')
        t0 = datetime.strptime(config[2], '%Y%m%d')
        t1 = datetime.strptime(config[3], '%Y%m%d')
        dlat = float(config[11])*111.11*1000
        dlon = float(config[12])*111.11*1000
        ddep = float(config[13])*111.11*1000

        
        Dlat = float(config[15])*111.11*1000
        Dlon = float(config[16])*111.11*1000
        Ddep = float(config[17])*111.11*1000

        DT = float(config[19])

        dt_filter = catalog[catalog['CC'] < 0.95]

        plt.figure()
        plt.plot(dt_filter['Date'], dt_filter['CC'], 'o')
        plt.show()

        
        print(file)
        print(t0)


        #catalog = pd.read_csv(file, delim_whitespace=True, header = 1, names=names, dtype=dtypes)
        #catalog.to_csv(file.replace('.dat', '.csv'), index=False)
