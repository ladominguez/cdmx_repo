import pandas as pd
import ssn
import pygmt
import sys

if len(sys.argv) < 2:
    input_file = 'DetectedFinal_All_20230501_20230531_mad_9_G_1_0.01_1_R_0.004_0.004_0.1_I_0.002_0.002_0.05_T_3.0_0_3.dat'
else:
    input_file = sys.argv[1]


region = '-99.216/-99.147/19.296/19.376'

def parse_parameters(input_file):
    parameters = input_file.split('_')
    config={}
    config['mad'] = float(parameters[5])
    config['R'] = float(parameters[11])
    config['I'] = float(parameters[15])
    return config

def plot_map(catalog, config):
    fig = pygmt.Figure()
    pygmt.config(MAP_FRAME_TYPE="plain")
    pygmt.config(FORMAT_GEO_MAP="ddd.xxx")
    fig.basemap(region=region, projection='M5i', frame=['WSen', 'xa0.015','ya0.015'])
    #fig.plot(x=catalog['longitude'].to_list(), y=catalog['latitude'].to_list(), style='c0.3c', pen='0.5p,black', fill='red')
    fig.plot('../coordinates/insurgentes.dat',pen='1p,black')
    fig.plot('../coordinates/periferico.dat',pen='1p,black')
    fig.plot('../coordinates/revolucion.dat',pen='1p,black')
    fig.plot('../coordinates/alta_tension.dat',pen='1p,black')
    fig.plot('../coordinates/circuito_interior.dat',pen='1p,black')
    fig.plot('../coordinates/fault.dat',pen='2p,black')
    

    lon = []
    lat = []

    for _, row in catalog.iterrows():
        if row['CC'] >= 0.95:
            lon.append(row['longitude'])
            lat.append(row['latitude'])
            fig.plot(x=float(row['longitude']), y=float(row['latitude']), style='c0.3c', pen='0.5p,black', fill='green')
            dlat = config['R']

            x_square = [row['longitude'] - dlat, row['longitude'] - dlat, row['longitude'] + dlat, row['longitude'] + dlat, row['longitude'] - dlat]
            y_square = [row['latitude'] - dlat, row['latitude'] + dlat, row['latitude'] + dlat, row['latitude'] - dlat, row['latitude'] - dlat]
            fig.plot(x=x_square, y=y_square, pen='0.5p,black')
    
    fig.savefig('map_dl_' + str(dlat) + '.png')

if __name__ == '__main__':
    catalog = ssn.read_MF_file(input_file, header=0)
    config = parse_parameters(input_file)
    print('input file read: ', input_file)
    print('config: ', config)
    plot_map(catalog, config)

    pass
