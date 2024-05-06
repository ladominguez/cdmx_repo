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

def plot_map(catalogo1, catalogo2):
    # For picking points on the map
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    # cid = fig.canvas.mpl_connect('button_press_event', mouse_event)

    for shape in sf.shapeRecords():
        x_utm = [i[0] for i in shape.shape.points[:]]
        y_utm = [i[1] for i in shape.shape.points[:]]
        lon, lat = proj_utm(x_utm, y_utm, inverse=True)
        ax.plot(lon, lat, linewidth=0.5, color='black')


    for lat1, lon1, lat2, lon2 in zip(catalogo1[:, 1], catalogo1[:, 2], catalogo2[:, 1], catalogo2[:, 2]):
        ax.plot([lon1, lon2], [lat1, lat2], 'k-', linewidth=0.5)

    for lat, lon in zip(catalogo1[:, 1], catalogo1[:, 2]):
        ax.plot(lon, lat, 'ro', markersize=marker_size)

    for lat, lon in zip(catalogo2[:, 1], catalogo2[:, 2]):
        ax.plot(lon, lat, 'go', markersize=marker_size)


    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_xlim(-99.22, -99.15)
    ax.set_ylim(19.340, 19.410)
    ax.set_aspect('equal', adjustable='box')
    ax.text(-99.18809090909091,19.381363636363634,'Insurgentes', fontsize=12, rotation=85, ma='left', va='bottom')
    ax.text(-99.16904545454545, 19.35781818181818,'Circuito Interior', fontsize=12, rotation=-5, ma='left', va='bottom')
    ax.text(-99.20659090909092, 19.368181818181817,'Alta Tension', fontsize=12, rotation=75, ma='left', va='bottom')
    ax.text(-99.20440909090909, 19.341590909090908,'Periferico', fontsize=12, rotation=80, ma='left', va='bottom')
    fig.savefig('map_catalog_shifted.png')
    print('Map saved as map_catalog_shifted.png')


if __name__ == '__main__':
    catalog_original = np.loadtxt('catalogs/catalog.dat')
    catalog_shifted = np.loadtxt('catalogs/catalog.may_shifted')

    plot_map(catalog_original, catalog_shifted)

    pass
