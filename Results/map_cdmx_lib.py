import shapefile as shp  # Requires the pyshp package
from pyproj import Proj, transform
from matplotlib import pyplot as plt
import geopy
import geopy.distance

zone = 14
sf = shp.Reader("/Users/antonio/Dropbox/Geofisica/Research/cdmx_repo/Results/zip/1ra_Red_vial_primaria_acceso_controlado_cdmx_09_23.shp")
proj_string = "+proj=utm +zone={} +ellps=WGS84".format(zone)
proj_utm = Proj(proj_string)

network = {'BJVM': (19.375,  -99.1707),
            'PZIG': (19.329,  -99.178),
            'COVM': (19.3511, -99.1562),
            'MHVM': (19.4080, -99.2091),
            'ENP8': (19.3669, -99.1931)}

def plot_map():
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
    ax.text(-99.178500000000000, 19.38000000000000,'Insurgentes', fontsize=12, rotation=76, ma='left', va='bottom')
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

def plot_catalog_detections(fig, ax, catalog, color='red', marker_size=10):
    for _, row in catalog.iterrows():
        if row['Reference'][0:6] == '202305':
            ax.plot(float(row['longitude']), float(row['latitude']), 'ko', markersize=6, alpha=0.5, markerfacecolor='red')
        elif row['Reference'][0:6] == '202312':
            ax.plot(float(row['longitude']), float(row['latitude']), 'ko', markersize=6, alpha=0.5, markerfacecolor='blue')
        else:
            print(f"Unknown template {row['Reference']}")
    return fig, ax

def plot_mainshock(fig, ax, catalog, color='yellow', marker_size=10):
    idx = catalog['magnitude'].idxmax()
    ax.plot(catalog['longitude'][idx], catalog['latitude'][idx], 'k*', markersize=marker_size, markerfacecolor=color)
    return fig, ax

def plot_mainshock_december_14(fig, ax,  color='yellow', marker_size=10):
    ax.plot(-99.199, 19.365, 'k*', markersize=marker_size, markerfacecolor=color)
    return fig, ax

def plot_fault_trace(fig, ax, eq_name='both'):
    if eq_name == 'may':
        ax.plot((-99.20175, -99.17747),(19.360931, 19.366446), 'k-', lw=2)
    elif eq_name == 'december':
        ax.plot((-99.1997, -99.1844),(19.3707, 19.3721), 'k-', lw=2)
    elif eq_name == 'both':
        ax.plot((-99.20175, -99.17747),(19.360931, 19.366446), 'k-', lw=2, color = 'darkred')
        ax.plot((-99.1997, -99.1844),(19.3707, 19.3721), 'k-', lw=2, color = 'darkblue')
    else:
        print(f"Unknown fault trace {eq_name}")
    return fig, ax

def plot_scale(fig,ax):
    One_km = 0.0095 # 360/(6371*cos(19))
    midpoint = (-99.17, 19.35)
    ax.plot([midpoint[0] - One_km/2, midpoint[0] + One_km/2], [midpoint[1], midpoint[1]], 'k-', lw=2)
    ax.text(midpoint[0], midpoint[1]+0.001, '1 km', fontsize=12, ha='center', va='bottom')
    return fig, ax

def plot_pie_chart(fig, ax, catalog, no_templates):
    axins = ax.inset_axes([0.75, 0.75, 0.25, 0.25])

    try:
        count_may = catalog['Reference'].str.contains('202305').value_counts()[True]
    except:
        count_may = 0
    
    try:
        count_decemeber = catalog['Reference'].str.contains('202312').value_counts()[True]
    except:
        count_decemeber = 0

    #try:
    #    count_may, count_decemeber = catalog['Reference'].str.contains('202305').value_counts()
    #except ValueError:
    #    count_may = catalog['Reference'].str.contains('202305').value_counts()
    #    count_decemeber = 0
    sizes = [count_may, count_decemeber, no_templates]
    labels = f'May ({count_may})', f'December ({count_decemeber})', f'Templates ({no_templates})'   
    axins.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    return fig, ax, count_may, count_decemeber

def plot_bearings(fig, ax, bearings):
    for station, bearing in bearings.items():
        pt1 = geopy.Point(network[station])
        pt2 = geopy.distance.distance(kilometers=20).destination(pt1, bearing)
        ax.plot([pt1.longitude, pt2.longitude], [pt1.latitude, pt2.latitude], 'k--', lw=1.5, color='dimgray')
        if station == 'ENP8':
            pt2 = geopy.distance.distance(kilometers=20).destination(pt1, bearing + 180) 
            ax.plot([pt1.longitude, pt2.longitude], [pt1.latitude, pt2.latitude], 'k--', lw=1.5, color='dimgray')
    return fig, ax

if __name__ == '__main__':
    fig, ax = plot_map(stations=['BJVM', 'PZIG', 'COVM', 'MHVM', 'ENP8'])
    fig, ax = add_stations(fig, ax, ['BJVM', 'PZIG', 'COVM', 'MHVM', 'ENP8'])
    
    fig.show()

    