import pandas as pd
import folium
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.cm as cm
import branca
import os
colormap = cm.hot

cc_lim = 0.68
mad = 9.2

config = 'mad_9_G_1_0.01_1_R_0.005_0.005_0.1_I_0.0025_0.0025_0.05_T_2.0_0_2'
config = 'mad_9_G_1_0.01_1_R_0.003_0.003_0.1_I_0.0015_0.0015_0.05_T_2.0_0_2'
config = 'mad_9_G_1_0.01_1_R_0.004_0.004_0.1_I_0.002_0.002_0.05_T_3.0_0_3'
config = 'mad_9_G_1_0.01_1_R_0_0_0_I_0.0015_0.0015_0.05_T_2.0_0_2'
config = 'mad_9_G_1_0.01_1_R_0.004_0.004_0.1_I_0.002_0.002_0.05_T_2.0_0_2'

# December
#config = 'mad_9_G_1_0.01_1_R_0.002_0.002_0.1_I_0.001_0.001_0.05_T_2.0_0_2'
#config = 'mad_9_G_1_0.01_1_R_0.003_0.003_0.1_I_0.0015_0.0015_0.05_T_2.0_0_2'
#config = 'mad_9_G_1_0.01_1_R_0.004_0.004_0.1_I_0.002_0.002_0.05_T_2.0_0_2'
#config = 'mad_9_G_1_0.01_1_R_0.003_0.003_0.1_I_0.0015_0.0015_0.05_T_2.0_0_2'
config = 'mad_9_G_1_0.01_2_R_0.0021_0.0021_0.1_I_0.0007_0.0007_0.05_T_2.0_0_2'

# All
#config = 'mad_9_G_1_0.01_2_R_0.0021_0.0021_0.1_I_0.0007_0.0007_0.05_T_2.0_0_2'
#prefix = 'All_20230101_20231231_'
prefix = 'DecemberAllTemplates_20231201_20231231_'

#input_file = os.path.join('December_20231201_20231231_' + config,'Detected_December_20231201_20231231_' + config + '.dat')
input_file = os.path.join('outputs', f"Detected_{prefix}{config}.dat")
input_file = "./Results/DetectedFinal_All_20230501_20230531_mad_9_G_1_0.01_1_R_0.004_0.004_0.1_I_0.002_0.002_0.05_T_3.0_0_3.dat"
#input_file = "./Results/Detected_JanuaryMay_20230101_20230531_mad_9_G_1_0.01_2_R_0.004_0.004_0.1_I_0.002_0.002_0.05_T_3.0_0_3.dat"
print('input_file: ', input_file)

repeaters_flag = False

if repeaters_flag:
    repeaters_file = os.path.join('possible_repeaters.dat') 
    repeater = [19.3620,  -99.2060]


top3 = os.path.join(config,'top3.dat')
print('top3:', top3)

names = ['No', 'Date', 'Time', 'latitude', 'longitude', 'Depth', 'Mag', 'CC', 'MAD', 'Reference']
dtypes = {'No': int, 'Date': str, 'Time': str, 'latitude': float, 'longitude': float, 'Depth': float, 'Mag': float,
          'CC': float, 'MAD': float, 'Reference': str}

if __name__ ==  '__main__':
    print('input_file:', input_file)
    try:
        catalog =  pd.read_csv(input_file, delim_whitespace=True, header = 1, names=names, dtype=dtypes)
    except FileNotFoundError:
        print('File does not exist')
        exit()

    catalog = catalog[catalog['MAD'] >= mad]

    catalog_temp = pd.read_csv('catalog_may.dat', delim_whitespace=True, names = ['date', 'latitude', 'longitude', 'Depth', 'Mag', 'latitude2', 'longitude2', 'depth2'],
                               dtype={'date': str, 'latitude': float, 'longitude': float, 'Depth': float, 'Mag': float, 'latitude2': float, 'longitude2': float, 'depth2': float})
    catalog_temp['Date'] = pd.to_datetime(catalog_temp['date'], format='%Y%m%d%H%M%S.%f')

    #top3 = pd.read_csv(top3, delim_whitespace=True, names=['N','Reference'], dtype = {'N': int,'Reference': str})

    catalog['Date'] = catalog['Date'].str.cat(catalog['Time'], sep=' ')
    catalog['Date'] = pd.to_datetime(catalog['Date'], format='%Y/%m/%d %H:%M:%S.%f')
    catalog = catalog.drop(columns=['Time'])

    if repeaters_flag:
        repeaters = pd.read_csv(repeaters_file, delim_whitespace=True, names=names, dtype=dtypes)
        repeaters['Date'] = repeaters['Date'].str.cat(repeaters['Time'], sep=' ')
        repeaters['Date'] = pd.to_datetime(repeaters['Date'], format='%Y/%m/%d %H:%M:%S.%f')
        repeaters = repeaters.drop(columns=['Time'])

    norm = plt.Normalize(catalog['Depth'].min(), catalog['Depth'].max())
    depths = catalog['Depth']
    #print(catalog.head())
    
    m = folium.Map(location=(19.362414,-99.201035), zoom_start=14)
    k = 0
    colormap = branca.colormap.LinearColormap(colors=['blue', 'green', 'yellow', 'red'], 
                                          index=depths.quantile([0.25, 0.5, 0.75]), 
                                          vmin=depths.min(), 
                                          vmax=depths.max())
    
    colormap2 = branca.colormap.linear.YlOrRd_09.scale(0,2)
    colormap2 = colormap2.to_step(index=[0,0.250,0.500,0.750,1.000,1.250,1.500,1.750,2.000])
    colormap2.add_to(m)
    colormap2.caption = 'Depth (km)'

    for index, row in catalog.iterrows():
        if row['CC'] < cc_lim:
            #color = colormap(row['Depth'])
            color = colormap2(row['Depth'])
            #color = color[:3]
            #color = 'rgb(' + str(int(color[0]*255)) + ',' + str(int(color[1]*255)) + ',' + str(int(color[2]*255)) + ')'

            folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=6,
                            color=color,
                            popup=row['Date'].strftime('%Y/%m/%d %H:M:S') + ' ' + str(row['Mag']),
                            fill_color=color, 
                           ).add_to(m)
    for index, row in catalog.iterrows():
        if row['CC'] > cc_lim:
            # Using folium.CircleMarker fill marker colorcoded by depth
            #color = colormap(row['Depth']) 
            color = colormap2(row['Depth']) 
            #color = colormap(norm(row['Depth']))
            #color = color[:3]
            #color = 'rgb(' + str(int(color[0]*255)) + ',' + str(int(color[1]*255)) + ',' + str(int(color[2]*255)) + ')'
            folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=6,
                            color='black',
                            popup=row['Date'].strftime('%Y/%m/%d %H:M:S') + ' ' + str(row['Mag']),
                            fill_color=color, # divvy color
                           ).add_to(m)
    #for index, row in top3.iterrows():
    #    subcat = catalog.loc[catalog['Reference']==row['Reference']]
    #    subcat.reset_index(drop=True, inplace=True)
    #    ind_max = subcat['MAD'].idxmax()
    #    folium.CircleMarker([subcat.iloc[ind_max]['latitude'], subcat.iloc[ind_max]['longitude']], popup=row['N'], fill_color='blue', radius = 20).add_to(m)
    folium.Marker(location=[19.375,  -99.1707], popup='BJVM').add_to(m)
    folium.Marker(location=[19.3511,  -99.1562], popup='COVM').add_to(m)
    folium.Marker(location=[19.4080, -99.2091], popup='MHVM').add_to(m)
    folium.Marker(location=[19.3669, -99.1931], popup='ENP8').add_to(m)
    folium.Marker(location=[19.329,  -99.178 ], popup='PZIG').add_to(m)

    if repeaters_flag:
        folium.CircleMarker(repeater, fill_color='red', fill_opacity=1,radius = 10, weigth=5, opacity=1, popup='Repeater').add_to(m)

    fig, ax = plt.subplots(3, 1, figsize=(16, 6), sharex=True)
    plt.subplots_adjust(wspace=0, hspace=0)
    markerlines, stemlines, _ = ax[0].stem(catalog['Date'], catalog['Mag'], 'o', linefmt='--', basefmt='black')
    plt.setp(stemlines, 'linewidth', 1)
    plt.setp(markerlines, 'markeredgecolor', 'black')

    catalog_counter = 0
    for index, row in catalog.iterrows():
        if row['CC'] > cc_lim:
            ax[0].plot(row['Date'], row['Mag'], 'o', color='darkorange', markersize=9, markeredgecolor='black')
            catalog_counter += 1
        else:
            #pass
            ax[0].plot(row['Date'], row['Mag'], 'o', color='navy', markersize=7, markeredgecolor='black')

    print('No of templates:', catalog_counter)

    if repeaters_flag:
        for index, row in repeaters.iterrows():
            print(row['Date'], row['Mag'])
            ax[0].plot(row['Date'], row['Mag'], 'k*', mec='black', mfc='yellow', markersize=12)


    ax[0].set_xlabel('Date')
    ax[0].set_ylabel('Magnitude', fontsize = 14)
    #ax[0].set_title(u'Template Matching Catalog for MAD ≥' + str(mad))
    ax[0].set_ylim([0, 3.2])
    ax[0].set_yticklabels(ax[0].get_yticklabels(), fontsize=12)
    ax[0].grid(True)
    #ax[0].set_ylabels = ['', '1', '2', '3']
    ax[0].set_ylim([0, 3.4])
    yticks_ax0 = ax[0].yaxis.get_major_ticks()
    yticks_ax0[0].label1.set_visible(False)
    #yticks_ax0 = ax[0].yaxis.get_major_ticks()
    #yticks_ax0[-1].label.set_visible(False)
    # plot colorcoded by magnitude and add colorbar
    # ax[1].scatter(catalog['Date'], catalog['Depth'], c=catalog['Mag'], s=5)
    cax = inset_axes(ax[1], width="2%", height="100%", loc='upper right', borderpad=0)
    #scatter = ax[1].scatter(catalog['Date'], catalog['Depth'], c=catalog['Mag'], s=catalog['Mag']*5, cmap='hot_r',edgecolor='black')

    template_detection = catalog.loc[catalog['CC'] >= cc_lim]
    scatter = ax[1].scatter(template_detection['Date'], template_detection['Depth'], c=template_detection['Mag'], s=template_detection['Mag']*30, cmap='hot_r',edgecolor='black', marker='s')
    scatter = ax[1].scatter(catalog_temp['Date'], catalog_temp['Depth'], c=catalog_temp['Mag'], s=catalog_temp['Mag']*30, cmap='hot_r',edgecolor='black', marker='s')
    cbar = plt.colorbar(scatter, ax=ax[1],cax=cax)

    all_detection = catalog.loc[catalog['CC'] < cc_lim]
    all_Templates = catalog.loc[catalog['CC'] >= cc_lim]
    scatter = ax[1].scatter(all_detection['Date'], all_detection['Depth'], c=all_detection['Mag'], s=all_detection['Mag']*30, cmap='hot_r',edgecolor='black')

    if repeaters_flag:
        ax[1].plot(repeaters['Date'], repeaters['Depth'], 'k*', mec='black', mfc='yellow', markersize=16)
    cbar.set_label('Magnitude', fontsize=14)

    #ax[1].set_xlabel('Date')
    ax[1].set_ylabel('Depth', fontsize = 14)
    ax[1].invert_yaxis()
    ax[1].set_yticklabels(ax[1].get_yticklabels(), fontsize=12)
    ax[1].grid(True)

    cax2 = inset_axes(ax[2], width="2%", height="100%", loc='upper right', borderpad=0)
    scatter2 = ax[2].scatter(all_detection['Date'], all_detection['Depth'], c=all_detection['MAD'], s=all_detection['MAD']*10, cmap='hot_r',edgecolor='black', marker='s')
    scatter2 = ax[2].scatter(all_Templates['Date'], all_Templates['Depth'], c=all_Templates['MAD'], s=all_Templates['MAD']*2,  cmap='hot_r',edgecolor='black', marker='D')
    cbar2 = plt.colorbar(scatter2, ax=ax[2],cax=cax2)
    cbar2.set_label('MAD', fontsize=14)
    #ax[2].set_xlabel('Date', fontsize=14)
    ax[2].set_ylabel('Depth', fontsize=14)
    ax[2].set_xticklabels(ax[2].get_xticklabels(), rotation=-15, ha='left', fontsize=14)
    ax[2].set_yticklabels(ax[2].get_yticklabels(), fontsize=12)
    ax[2].invert_yaxis()
    ax[2].grid(True)

    plt.savefig(f'Figure_Final_{config}.png', dpi=500)
    print(f'Saved Figure_Final_{config}.png')
    #m.show_in_browser()
    m.save(f'map_Final_{config}.html')  
    print(f'Saved map_mad_December_{config}.html')
