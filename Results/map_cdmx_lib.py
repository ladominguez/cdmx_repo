import shapefile as shp  # Requires the pyshp package
from pyproj import Proj, transform
from matplotlib import pyplot as plt


zone = 14
sf = shp.Reader("./zip/1ra_Red_vial_primaria_acceso_controlado_cdmx_09_23.shp")
proj_string = "+proj=utm +zone={} +ellps=WGS84".format(zone)
proj_utm = Proj(proj_string)

network = {'BJVM': (19.375,  -99.1707),
            'PZIG': (19.329,  -99.178),
            'COVM': (19.3511, -99.1562),
            'MHVM': (19.4080, -99.2091),
            'ENP8': (19.3669, -99.1931)}

def plot_map(stations=None):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))

    for shape in sf.shapeRecords():
        x_utm = [i[0] for i in shape.shape.points[:]]
        y_utm = [i[1] for i in shape.shape.points[:]]
        lon, lat = proj_utm(x_utm, y_utm, inverse=True)
        ax.plot(lon, lat, linewidth=0.5, color='black')

    lon = []
    lat = []

    ax.set_xlabel('Longitude (°)')
    ax.set_ylabel('Latitude (°)')
    ax.set_xlim(-99.22, -99.15)
    ax.set_ylim(19.340, 19.410)
    ax.set_aspect('equal', adjustable='box')
    ax.text(-99.18809090909091,19.381363636363634,'Insurgentes', fontsize=12, rotation=85, ma='left', va='bottom')
    ax.text(-99.16904545454545, 19.35781818181818,'Circuito Interior', fontsize=12, rotation=-5, ma='left', va='bottom')
    ax.text(-99.20659090909092, 19.368181818181817,'Alta Tension', fontsize=12, rotation=75, ma='left', va='bottom')
    ax.text(-99.20440909090909, 19.341590909090908,'Periferico', fontsize=12, rotation=80, ma='left', va='bottom')
    return fig, ax

def add_stations(fig, ax, stations):

    for station in stations:
        try: 
            latitiude, longitude = network[station]
        except KeyError:
            print(f"Station {station} not found in network")
            continue
        ax.plot(longitude, latitiude, 'k^', markersize=10, alpha=0.85, markerfacecolor='blue', lw=2)
        ax.text(longitude, latitiude, station, fontsize=12, ha='right', va='bottom')
    return fig, ax

def plot_catalog_templates(fig, ax, catalog, color='red', marker_size=10):
    for _, row in catalog.iterrows():
        ax.plot(float(row['longitude']), float(row['latitude']), 'ko', markersize=6, alpha=0.5, markerfacecolor=color)
    return fig, ax

def plot_mainshock(fig, ax, catalog, color='yellow', marker_size=10):
    idx = catalog['magnitude'].idxmax()
    ax.plot(catalog['longitude'][idx], catalog['latitude'][idx], 'k*', markersize=marker_size, markerfacecolor=color)
    return fig, ax

def plot_fault_trace(fig, ax, eq_name='may'):
    if eq_name == 'may':
        ax.plot((-99.20175, -99.17747),(19.360931, 19.366446), 'k-', lw=2)
    elif eq_name == 'december':
        ax.plot((-99.1997, -99.1844),(19.3707, 19.3721), 'k-', lw=2)
    return fig, ax

def plot_scale(fig,ax):
    One_km = 0.0095 # 360/(6371*cos(19))
    midpoint = (-99.17, 19.35)
    ax.plot([midpoint[0] - One_km/2, midpoint[0] + One_km/2], [midpoint[1], midpoint[1]], 'k-', lw=2)
    ax.text(midpoint[0], midpoint[1]+0.001, '1 km', fontsize=12, ha='center', va='bottom')
    return fig, ax

if __name__ == '__main__':
    fig, ax = plot_map(stations=['BJVM', 'PZIG', 'COVM', 'MHVM', 'ENP8'])
    fig, ax = add_stations(fig, ax, ['BJVM', 'PZIG', 'COVM', 'MHVM', 'ENP8'])
    
    fig.show()

    