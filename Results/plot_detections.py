from map_cdmx_lib import plot_map, add_stations, plot_catalog_templates, plot_fault_trace, plot_mainshock, plot_scale, plot_catalog_detections, plot_pie_chart
from TM_utils import load_TM_catalog
import pandas as pd

input_file = '../outputs/Detected_MayAllTemplates_20230501_20230531_mad_9_G_1_0.01_2_R_0.0021_0.0021_0.1_I_0.0007_0.0007_0.05_T_2.0_0_2.dat'
MAD_min = 10
month = 'May'

input_file = '../outputs/Detected_DecemberAllTemplates_20231201_20231231_mad_9_G_1_0.01_2_R_0.0021_0.0021_0.1_I_0.0007_0.0007_0.05_T_2.0_0_2.dat'
MAD_min = 10
month = 'December'
# Load the data


if __name__ == '__main__':
    detections_may, no_templates = load_TM_catalog(input_file, exclude_templates=True, MAD_min=MAD_min)
    fig, ax = plot_map()
    fig, ax = add_stations(fig, ax, ['BJVM', 'PZIG', 'COVM', 'MHVM', 'ENP8'])
    fig, ax = plot_catalog_detections(fig, ax, detections_may, color='red', marker_size=10)
    fig, ax = plot_fault_trace(fig, ax, eq_name='may')
    fig, ax = plot_fault_trace(fig, ax, eq_name='december')
    #fig, ax = plot_mainshock(fig, ax, catalog_may, color='yellow', marker_size=18)
    #fig, ax = plot_mainshock(fig, ax, catalog_dec, color='lightgreen', marker_size=18)
    fig, ax = plot_scale(fig, ax)
    fig, ax, N_may, N_dec = plot_pie_chart(fig, ax, detections_may, no_templates)

    # markers for the detections
    ax.plot(-99.218, 19.382, 'ko', markersize=10, alpha=0.5, markerfacecolor='red')
    ax.plot(-99.218, 19.379, 'ko', markersize=10, alpha=0.5, markerfacecolor='blue')
    ax.text(-99.217, 19.382, f'May 2023 ({N_may} eqs.)', fontsize=12, ha='left', va='center')
    ax.text(-99.217, 19.379, f'December 2023 ({N_dec} eqs.)', fontsize=12, ha='left', va='center')

    ax.title.set_text(f'Detections {month} 2023\nMAD ≥ {MAD_min} (n={len(detections_may)+no_templates})')
    ax.title.set_fontweight('bold')
    fig.savefig(f'detections_{month}_mad_{MAD_min}.png', dpi=600)
    print(f'Saving detections_{month}_mad_{MAD_min}.png')

    pass
