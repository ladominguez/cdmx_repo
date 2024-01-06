import pandas as pd
import folium
from datetime import datetime


input_file = 'dat/DetectedFinal_All_20230501_20230531.dat'
if __name__ ==  '__main__':

    catalog = pd.read_csv(input_file, delim_whitespace=True, header = 1, 
                         names=['No', 'Date', 'Time', 'latitude', 'longitude', 'Depth', 'Mag', 'CC', 'MAD', 'Reference'],
                         dtype={'No': int, 'Date': str, 'Time': str, 'latitude': float, 'longitude': float, 'Depth': float, 'Mag': float, 'CC': float, 'MAD': float, 'Reference': str})

    catalog['Date'] = catalog['Date'].str.cat(catalog['Time'], sep=' ')
    catalog['Date'] = pd.to_datetime(catalog['Date'], format='%Y/%m/%d %H:%M:%S.%f')
    catalog = catalog.drop(columns=['Time'])
    #print(catalog.head())
    
    m = folium.Map(location=(19.432608, -99.133209), zoom_start=12)
    k = 0
    for index, row in catalog.iterrows():
        if row['CC'] > 0.98:
            k = k + 1
            folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=6,
                            popup=row['Date'].strftime('%Y/%m/%d %H:M:S') + ' ' + str(row['Mag']),
                            fill_color="#3db7e4", # divvy color
                           ).add_to(m)
    print('K:', k)
    m.show_in_browser()