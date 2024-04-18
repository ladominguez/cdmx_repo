import pandas as pd
import ssn
from matplotlib import pyplot as plt
#import pygmt
import sys
import numpy as np

import shapefile as shp  # Requires the pyshp package
from pyproj import Proj, transform

if len(sys.argv) < 2:
    input_file = 'DetectedFinal_All_20230501_20230531_mad_9_G_1_0.01_1_R_0.004_0.004_0.1_I_0.002_0.002_0.05_T_3.0_0_3.dat'
else:
    input_file = sys.argv[1]


region = '-99.22/-99.15/19.340/19.410'

zone = 14
sf = shp.Reader("./zip/1ra_Red_vial_primaria_acceso_controlado_cdmx_09_23.shp")
proj_string = "+proj=utm +zone={} +ellps=WGS84".format(zone)
proj_utm = Proj(proj_string)
fault = np.loadtxt('../coordinates/fault.dat')
marker_size = 8

def mouse_event(event):
    print('x: {} and y: {}'.format(event.xdata, event.ydata))

def parse_parameters(input_file):
    parameters = input_file.split('_')
    config={}
    config['mad'] = float(parameters[5])
    config['R'] = float(parameters[11])
    config['I'] = float(parameters[15])
    return config

def plot_map(catalog, config):
    #fig = pygmt.Figure()
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    cid = fig.canvas.mpl_connect('button_press_event', mouse_event)
    #pygmt.config(MAP_FRAME_TYPE="plain")
    #pygmt.config(FORMAT_GEO_MAP="ddd.xxx")
    #fig.basemap(region=region, projection='M5i', frame=['WSen', 'xa0.015','ya0.015'])
    #fig.plot(x=catalog['longitude'].to_list(), y=catalog['latitude'].to_list(), style='c0.3c', pen='0.5p,black', fill='red')

    for shape in sf.shapeRecords():
        x_utm = [i[0] for i in shape.shape.points[:]]
        y_utm = [i[1] for i in shape.shape.points[:]]
        lon, lat = proj_utm(x_utm, y_utm, inverse=True)
        ax.plot(lon, lat, linewidth=0.5, color='black')

    #fig.plot('../coordinates/insurgentes.dat',pen='1p,black')
    #fig.plot('../coordinates/periferico.dat',pen='1p,black')
    #fig.plot('../coordinates/revolucion.dat',pen='1p,black')
    #fig.plot('../coordinates/alta_tension.dat',pen='1p,black')
    #fig.plot('../coordinates/circuito_interior.dat',pen='1p,black')
    #fig.plot('../coordinates/fault.dat',pen='2p,black')
    

    lon = []
    lat = []

    for _, row in catalog.iterrows():
        if row['CC'] < 0.95:
            ax.plot(float(row['longitude']), float(row['latitude']), 'ko', markersize=6, alpha=0.5, markerfacecolor='gray')

    for _, row in catalog.iterrows():
        if row['CC'] >= 0.95:
            lon.append(row['longitude'])
            lat.append(row['latitude'])
            ax.plot(float(row['longitude']), float(row['latitude']), 'ko', markersize=10, alpha=0.85, markerfacecolor='red', lw=2)
            dlat = config['R']
            dinc = config['I']

            x_square = [row['longitude'] - dlat, row['longitude'] - dlat, row['longitude'] + dlat, row['longitude'] + dlat, row['longitude'] - dlat]
            y_square = [row['latitude'] - dlat, row['latitude'] + dlat, row['latitude'] + dlat, row['latitude'] - dlat, row['latitude'] - dlat]
            x_inc = [row['longitude'] - dinc, row['longitude'] - dinc, row['longitude'] + dinc, row['longitude'] + dinc, row['longitude'] - dinc]
            y_inc = [row['latitude'] - dinc, row['latitude'] + dinc, row['latitude'] + dinc, row['latitude'] - dinc, row['latitude'] - dinc]
            x_inc2 = [row['longitude'] - dlat, row['longitude'] - dlat, row['longitude'] + dlat, row['longitude'] + dlat, row['longitude'] - dlat]
            y_inc2 = [row['latitude'] - dinc, row['latitude'] + dinc, row['latitude'] + dinc, row['latitude'] - dinc, row['latitude'] - dinc]
            x_inc3 = [row['longitude'] - dinc, row['longitude'] - dinc, row['longitude'] + dinc, row['longitude'] + dinc, row['longitude'] - dinc]
            y_inc3 = [row['latitude'] - dlat, row['latitude'] + dlat, row['latitude'] + dlat, row['latitude'] - dlat, row['latitude'] - dlat]
            x_inc4 = [row['longitude']      , row['longitude']      , row['longitude']      , row['longitude']      , row['longitude']      ]
            y_inc4 = [row['latitude'] - dinc, row['latitude'] + dinc, row['latitude'] + dinc, row['latitude'] - dinc, row['latitude'] - dinc]
            x_inc5 = [row['longitude'] - dinc, row['longitude'] - dinc, row['longitude'] + dinc, row['longitude'] + dinc, row['longitude'] - dinc]
            y_inc5 = [row['latitude']        , row['latitude']        , row['latitude']        , row['latitude']        , row['latitude']        ]
            x_inc5 = [row['longitude']       , row['longitude']       , row['longitude'] + dlat, row['longitude'] - dlat, row['longitude']]
            y_inc5 = [row['latitude']  +dlat , row['latitude']  - dlat, row['latitude']        , row['latitude']        , row['latitude'] ]
            x_inc6 = [row['longitude']       , row['longitude']       , row['longitude'] + dinc, row['longitude'] - dinc, row['longitude']]
            y_inc6 = [row['latitude']  +dinc , row['latitude']  - dinc, row['latitude']        , row['latitude']        , row['latitude'] ]
            ax.plot(x_square, y_square, 'k-', linewidth=1.5)
            ax.plot(x_square, y_square, 'r+', linewidth=1, markersize=marker_size)
            ax.plot(x_inc, y_inc, 'r+', linewidth=1, markersize=marker_size)
            ax.plot(x_inc2, y_inc2, 'r+', linewidth=1, markersize=marker_size)
            ax.plot(x_inc3, y_inc3, 'r+', linewidth=1, markersize=marker_size)
            ax.plot(x_inc4, y_inc4, 'r+', linewidth=1, markersize=marker_size)
            ax.plot(x_inc5, y_inc5, 'r+', linewidth=1, markersize=marker_size)
            ax.plot(x_inc6, y_inc6, 'r+', linewidth=1, markersize=marker_size)
        
    #ax.plot(fault[:,0], fault[:,1], 'r+', linewidth=1, markersize=12)
    #ax.plot(-99.190, 19.369, 'k*', markersize=18, alpha=0.5, markerfacecolor='yellow')
    #ax.plot(-99.199, 19.363, 'k*', markersize=18, alpha=0.5, markerfacecolor='green')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_xlim(-99.22, -99.15)
    ax.set_ylim(19.340, 19.410)
    ax.set_aspect('equal', adjustable='box')
    ax.title.set_text('DL: ' + str(np.round(dlat*111.1*1000)) +  'm I: ' + str(np.round(config['I']*111.1*1000)) + 'm MAD: ' + str(config['mad']) )
    ax.text(-99.18809090909091,19.381363636363634,'Insurgentes', fontsize=12, rotation=85, ma='left', va='bottom')
    ax.text(-99.16904545454545, 19.35781818181818,'Circuito Interior', fontsize=12, rotation=-5, ma='left', va='bottom')
    ax.text(-99.20659090909092, 19.368181818181817,'Alta Tension', fontsize=12, rotation=75, ma='left', va='bottom')
    ax.text(-99.20440909090909, 19.341590909090908,'Periferico', fontsize=12, rotation=80, ma='left', va='bottom')
    #fig.show() 
    #fig.show() 
    fig.savefig('map_dl_' + str(np.round(dlat*111.1*1000)) + 'm.png')
    #fig.show() 
    fig.savefig('map_dl_' + str(np.round(dlat*111.1*1000)) + 'm.png')

if __name__ == '__main__':
    catalog = ssn.read_MF_file(input_file, header=0)
    config = parse_parameters(input_file)
    print('input file read: ', input_file)
    print('config: ', config)
    plot_map(catalog, config)

    pass
