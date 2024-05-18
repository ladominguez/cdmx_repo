from map_cdmx_lib import plot_map, add_stations, plot_catalog_templates, plot_fault_trace, plot_mainshock, plot_scale
import pandas as pd

names_catalog = ['eq_id',  'latitude', 'longitude', 'depth', 'magnitude']
dtypes_catalog = {'eq_id': 'str', 'latitude': 'float', 'longitude': 'float', 'depth': 'float', 'magnitude': 'float'}

if __name__ == '__main__':
    catalog_may = pd.read_csv('catalogs/catalog.may', header=0, usecols=['eq_id', 'latitude', 'longitude', 'depth', 'magnitude'], delim_whitespace=True, names=names_catalog, dtype=dtypes_catalog)
    catalog_dec = pd.read_csv('catalogs/catalog.december', header=0, usecols=['eq_id', 'latitude', 'longitude', 'depth', 'magnitude'], delim_whitespace=True, names=names_catalog, dtype=dtypes_catalog)
    fig, ax = plot_map(stations=['BJVM', 'PZIG', 'COVM', 'MHVM', 'ENP8'])
    fig, ax = add_stations(fig, ax, ['BJVM', 'PZIG', 'COVM', 'MHVM', 'ENP8'])
    fig, ax = plot_catalog_templates(fig, ax, catalog_may, color='red', marker_size=10)
    fig, ax = plot_catalog_templates(fig, ax, catalog_dec, color='blue', marker_size=10)
    fig, ax = plot_fault_trace(fig, ax, eq_name='may')
    fig, ax = plot_fault_trace(fig, ax, eq_name='december')
    fig, ax = plot_mainshock(fig, ax, catalog_may, color='yellow', marker_size=18)
    fig, ax = plot_mainshock(fig, ax, catalog_dec, color='lightgreen', marker_size=18)
    fig, ax = plot_scale(fig, ax)

    # markers for the templates
    ax.plot(-99.218, 19.388, 'k*', markersize=12,  markerfacecolor='yellow')
    ax.plot(-99.218, 19.385, 'k*', markersize=12,  markerfacecolor='lightgreen')


    # markers for the detections
    ax.plot(-99.218, 19.382, 'ko', markersize=10, alpha=0.5, markerfacecolor='red')
    ax.plot(-99.218, 19.379, 'ko', markersize=10, alpha=0.5, markerfacecolor='blue')



    ax.text(-99.217, 19.388, 'Mainshock May 2023', fontsize=12, ha='left', va='center')
    ax.text(-99.217, 19.385, 'Mainshock December 2023', fontsize=12, ha='left', va='center')
    ax.text(-99.217, 19.382, f'May 2023 ({len(catalog_may)})', fontsize=12, ha='left', va='center')
    ax.text(-99.217, 19.379, f'December 2023 ({len(catalog_dec)})', fontsize=12, ha='left', va='center')

    ax.title.set_text('Templates used for the TM method')


    #ax.plot()

    fig.show()