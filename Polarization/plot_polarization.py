from obspy import read
from matplotlib import pyplot as plt
import numpy as np
import sys

sys.path.append('../Results')
from map_cdmx_lib import plot_map, add_stations, plot_fault_trace, plot_mainshock_december_14, plot_scale, plot_bearings

# Stations
stations = ['PZIG', 'BJVM', 'ENP8','COVM']
stations = ['ENP8']
window = {'PZIG': 0.25, 'BJVM': 0.20, 'ENP8': 0.15, 'COVM': 0.2}
r_sta  = {'PZIG': 50000, 'BJVM': 80000, 'ENP8': 30000, 'COVM': 10000}
bearing_offset = {'PZIG': 180, 'BJVM': 180, 'ENP8': 180, 'COVM': 0}
head_sta = {'PZIG': 5000, 'BJVM': 5000, 'ENP8': 1000, 'COVM': 1000}
color_arrow = {'PZIG': 'darkred', 'BJVM': 'darkorange', 'ENP8': 'teal', 'COVM': 'purple'}

eq_title = '2023-12-14 20:13:14.72 UTC'

#stations = ['COVM']
N_sta = len(stations)

def plot_polarization(stations, window, r_sta, bearing_offset, head_sta, color_arrow, eq_title):
    st = read('./20231214201314.72/*')
    fig, ax = plt.subplots(nrows=4,ncols=N_sta ,figsize=(4*N_sta, 11), squeeze=False)
    bearings = {}

    for k,station in enumerate(stations):

        print('Station:', station)
        tr_sta = st.select(station=station)
        north = tr_sta.select(component='N')[0]
        east = tr_sta.select(component='E')[0]
        vertical = tr_sta.select(component='Z')[0]

        p_time = vertical.stats.sac.a
        t = vertical.times()
        ind = np.where((t >= p_time) & (t < p_time + window[station]))[0]
        x_lim_max = np.max(t)
        x_lim_max = 7.5

        ax[0,k].plot(t, vertical.data, 'k', linewidth=0.5)
        ax[0,k].plot(t[ind], vertical.data[ind], 'r', linewidth=1)
        #ax[0].axvline(x=p_time, color='r', linestyle='--')
        ax[0,k].axvspan(p_time, p_time + window[station], color='r', alpha=0.35)
        ax[0,k].annotate('Vertical', xy = (0.05, 0.9), xytext=(0.05, .9),xycoords='axes fraction')
        ax[0,k].set_title(f'Station: {station}')
        ax[0,k].set_xlim(p_time - 0.1, x_lim_max)
        ax[0,k].grid('--', alpha=0.5, linewidth=0.5)
        ax[0,k].set_ylabel('Counts')
        ax[0,k].xaxis.set_tick_params(labelbottom=False)

        ax[1,k].plot(t, north.data, 'k', linewidth=0.5)
        ax[1,k].annotate('North', xy = (0.05, 0.9), xytext=(0.05, .9),xycoords='axes fraction')
        ax[1,k].axvspan(p_time, p_time + window[station], color='r', alpha=0.35)
        ax[1,k].set_xlim(p_time - 0.1, x_lim_max)
        ax[1,k].grid('--', alpha=0.5, linewidth=0.5)
        ax[1,k].set_ylabel('Counts')
        ax[1,k].xaxis.set_tick_params(labelbottom=False)

        pos1 = ax[0,k].get_position()
        pos2 = ax[1,k].get_position()
        pos3 = ax[2,k].get_position()

        gap = pos2.y1 - pos1.y0
        ax[1,k].set_position([pos2.x0, pos2.y0 - gap, pos2.width, pos2.height])

        ax[2,k].plot(t, east.data, 'k', linewidth=0.5)
        ax[2,k].annotate('East', xy = (0.05, 0.9), xytext=(0.05, .9),xycoords='axes fraction')
        ax[2,k].axvspan(p_time, p_time + window[station], color='r', alpha=0.35)
        ax[2,k].grid('--', alpha=0.5, linewidth=0.5)
        ax[2,k].set_xlim(p_time - 0.1, x_lim_max)

        ax[2,k].set_ylabel('Counts')
        ax[2,k].set_xlabel('Time (s)')

        pos2 = ax[1,k].get_position()
        pos3 = ax[2,k].get_position()

        gap = pos3.y1 - pos2.y0
        ax[2,k].set_position([pos3.x0, pos3.y0 - gap, pos3.width, pos3.height])

        ylim0 = ax[0,k].get_ylim()
        ylim1 = ax[1,k].get_ylim()
        ylim2 = ax[2,k].get_ylim()

        ax[0,k].set_ylim(np.min([ylim0[0], ylim1[0], ylim2[0]]), np.max([ylim0[1], ylim1[1], ylim2[1]]))
        ax[1,k].set_ylim(np.min([ylim0[0], ylim1[0], ylim2[0]]), np.max([ylim0[1], ylim1[1], ylim2[1]]))
        ax[2,k].set_ylim(np.min([ylim0[0], ylim1[0], ylim2[0]]), np.max([ylim0[1], ylim1[1], ylim2[1]]))
                       


        x = east.data[ind] - np.mean(east.data[ind])
        y = north.data[ind] - np.mean(north.data[ind])
        #y = vertical.data[ind] - np.mean(vertical.data[ind])

        direction = np.transpose(np.vstack(((x,y))))
        _, _, v1 = np.linalg.svd(direction)
        dir_vec1 = v1[0,:]

        bearing = np.degrees(np.arctan2(dir_vec1[1], dir_vec1[0]))
        print('Bearing:', bearing)

        r = r_sta[station]
        theta0 = bearing + bearing_offset[station]
        bearings[station] = 90 - theta0
        ax[3,k].plot(x, y, 'k', linewidth=0.5)

        pos4 = ax[3,k].get_position()
        ax[3,k].set_position([pos4.x0, 0.05, pos4.width, 1.5*pos4.height])

        ax[3,k].set_aspect('equal')
        ax[3,k].arrow(0, 0, r*np.cos(np.radians(theta0)), r*np.sin(np.radians(theta0)), color=color_arrow[station], width=0.35, length_includes_head=True, head_width=head_sta[station], head_length=head_sta[station])
        ax[3,k].annotate(f'{int(np.round(bearings[station]))}°', xy=(r*np.cos(np.radians(theta0)), r*np.sin(np.radians(theta0))), xytext=(r*np.cos(np.radians(theta0)), r*np.sin(np.radians(theta0))), color=color_arrow[station], fontsize=12)
        #ax[3,k].grid('--', alpha=0.5, linewidth=0.5)
        ax[3,k].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax[3,k].tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
        ax[3,k].spines['top'].set_visible(False)
        ax[3,k].spines['bottom'].set_visible(False)
        ax[3,k].spines['left'].set_visible(False)
        ax[3,k].spines['right'].set_visible(False)
        ax[3,k].set_xlabel('East')
        ax[3,k].set_ylabel('north')
        #ax[3,k].set_title(f'Window = {window[station]} s')  

        #fig.suptitle(f'Polarization Analysis - {eq_title}', fontsize=16)      

    return fig, ax, bearings

def plot_map_polarization():
    fig_map, ax_map = plot_map()
    fig_map, ax_map = add_stations(fig_map, ax_map, ['BJVM', 'COVM', 'MHVM', 'ENP8'])
    fig_map, ax_map = plot_bearings(fig_map, ax_map, bearings)
    fig_map, ax_map = plot_fault_trace(fig_map, ax_map, eq_name='both')
    fig_map, ax_map = plot_scale(fig_map, ax_map)
    ax_map.set_title(f'Polarization Analysis - {eq_title}', fontsize=16)
    fig_map, ax_map = plot_mainshock_december_14(fig_map, ax_map, color='yellow', marker_size=13)
    return fig_map, ax_map

    
if __name__ == '__main__':
    fig_pol, ax_pol, bearings = plot_polarization(stations, window, r_sta, bearing_offset, head_sta, color_arrow, eq_title)
    #_, _, bearings = plot_polarization(stations, window, r_sta, bearing_offset, head_sta, color_arrow, eq_title)
    #plot_map_polarization()

    #fig_pol.savefig('polarization_analysis_december14.png', dpi=500)
    #fig_map.savefig('polarization_analysis_map_december14.png', dpi=500)
    pass





