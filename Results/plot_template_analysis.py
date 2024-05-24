from map_cdmx_lib import plot_map, add_stations, plot_catalog_templates, plot_fault_trace, plot_mainshock, plot_scale, plot_catalog_detections, plot_pie_chart
from TM_utils import load_TM_catalog
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np



input_file = '../outputs/Detected_MayAllTemplates_20230501_20230531_mad_9_G_1_0.01_2_R_0.0021_0.0021_0.1_I_0.0007_0.0007_0.05_T_2.0_0_2.dat'
MAD_min = 9.3
month = 'May'

input_file = '../outputs/Detected_DecemberAllTemplates_20231201_20231231_mad_9_G_1_0.01_2_R_0.0021_0.0021_0.1_I_0.0007_0.0007_0.05_T_2.0_0_2.dat'
month = 'December'


cmap = mpl.colormaps['plasma']
colors= cmap(np.linspace(9, 30, 30))
norm = mpl.colors.Normalize(vmin=9, vmax=30)

colors_down = cmap(np.linspace(9, 11, 30))
norm_down = mpl.colors.Normalize(vmin=9, vmax=11)

if __name__ == '__main__':
    detections, no_templates = load_TM_catalog(input_file, exclude_templates=False)
    detections_per_template = detections['Reference'].value_counts()
    detections_per_template_sorted = detections_per_template.sort_index()
    
    ticks = list(range(0, len(detections_per_template_sorted)))
    ticks_labels = list(detections_per_template_sorted.index)

    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12, 10), sharex=True)
    plt.subplots_adjust(hspace=0)

    for k, (template, _) in enumerate(detections_per_template_sorted.items()):
        sub_cat = detections[detections['Reference'] == template]['MAD']
        for _, item_mad in sub_cat.items():
            if item_mad >= 11:
                ax[0].plot(k, item_mad, 'ko', markersize=10, alpha=0.5, mfc=cmap(norm(item_mad))[0:3])
            else:
                ax[1].plot(k, item_mad, 'ko', markersize=10, alpha=0.5, mfc=cmap(norm(item_mad))[0:3])

    ax[1].set_xticks(ticks, ticks_labels, rotation=90)
    for k, label in enumerate(ticks_labels):
        if '202305' in label:
            ax[1].get_xticklabels()[k].set_color("red")
        elif '202312' in label:
            ax[1].get_xticklabels()[k].set_color("blue")
        else:
            print(f"Unknown template {label}")
    ax[0].set_ylim(11, 30)
    ax[0].set_ylabel('MAD')

    ax0_b = ax[0].twinx()
    ax0_b.plot(ticks, detections_per_template_sorted.values, 'ko-', markersize=10, alpha=0.5, mfc='black')

    ax[1].set_ylim(9, 11)
    ax[1].axhline(y=9.3, color='r', linestyle='--', linewidth=2)
    ax[0].set_title(f'Detections per template - {month} 2023')
    ax[0].set_xlabel('Template')
    ax0_b.set_ylabel('Number of detections')
    ax[0].grid(linestyle='--', color='gray', alpha=0.5)
    ax[1].grid(linestyle='--', color='gray', alpha=0.5)
    ax[1].set_ylabel('MAD')
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical', pad=0.060, aspect=40)
    cbar.set_label('MAD')
    fig.savefig(f'detections_per_template_{month}.png', dpi=600, bbox_inches = 'tight')

    pass