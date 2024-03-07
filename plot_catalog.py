import pandas as pd
import folium
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.cm as cm
import branca
import os

colormap = cm.hot

#input_file = './MAD_09/dat/DetectedFinal_All_20230501_20230531.dat'
#input_file = './MAD_10/dat/DetectedFinal_All_20230501_20230531_mad_10.dat'

config = 'mad_9_G_1_0.01_1_R_0.005_0.005_0.1_I_0.0025_0.0025_0.05_T_2.0_0_2'
config = 'mad_9_G_1_0.01_1_R_0.003_0.003_0.1_I_0.0015_0.0015_0.05_T_2.0_0_2'
config = 'mad_9_G_1_0.01_1_R_0.004_0.004_0.1_I_0.002_0.002_0.05_T_3.0_0_3'
config = 'mad_9_G_1_0.01_1_R_0_0_0_I_0.0015_0.0015_0.05_T_2.0_0_2'
config = 'mad_9_G_1_0.01_1_R_0.004_0.004_0.1_I_0.002_0.002_0.05_T_2.0_0_2'
input_file = os.path.join(config,'DetectedFinal_All_20230501_20230531_' + config + '.dat') 

top3 = os.path.join(config,'top3.dat')
print('top3:', top3)

mad=9

if __name__ ==  '__main__':

    catalog = pd.read_csv(input_file, delim_whitespace=True, header = 1, 
                         names=['No', 'Date', 'Time', 'latitude', 'longitude', 'Depth', 'Mag', 'CC', 'MAD', 'Reference'],
                         dtype={'No': int, 'Date': str, 'Time': str, 'latitude': float, 'longitude': float, 'Depth': float, 'Mag': float, 'CC': float, 'MAD': float, 'Reference': str})
    top3 = pd.read_csv(top3, delim_whitespace=True, names=['N','Reference'], dtype = {'N': int,'Reference': str})

    catalog['Date'] = catalog['Date'].str.cat(catalog['Time'], sep=' ')
    catalog['Date'] = pd.to_datetime(catalog['Date'], format='%Y/%m/%d %H:%M:%S.%f')
    catalog = catalog.drop(columns=['Time'])
    norm = plt.Normalize(catalog['Depth'].min(), catalog['Depth'].max())
    depths = catalog['Depth']
    #print(catalog.head())
    
    m = folium.Map(location=(19.362414,-99.201035), zoom_start=14)
    k = 0
    colormap = branca.colormap.LinearColormap(colors=['blue', 'green', 'yellow', 'red'], 
                                          index=depths.quantile([0.25, 0.5, 0.75]), 
                                          vmin=depths.min(), 
                                          vmax=depths.max())

    for index, row in catalog.iterrows():
        if row['CC'] < 0.98:
            color = colormap(row['Depth'])
            #color = color[:3]
            #color = 'rgb(' + str(int(color[0]*255)) + ',' + str(int(color[1]*255)) + ',' + str(int(color[2]*255)) + ')'

            folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=6,
                            color=color,
                            popup=row['Date'].strftime('%Y/%m/%d %H:M:S') + ' ' + str(row['Mag']),
                            fill_color=color, 
                           ).add_to(m)
    for index, row in catalog.iterrows():
        if row['CC'] > 0.98:
            # Using folium.CircleMarker fill marker colorcoded by depth
            color = colormap(row['Depth']) 
            #color = colormap(norm(row['Depth']))
            #color = color[:3]
            #color = 'rgb(' + str(int(color[0]*255)) + ',' + str(int(color[1]*255)) + ',' + str(int(color[2]*255)) + ')'
            folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=6,
                            color=color,
                            popup=row['Date'].strftime('%Y/%m/%d %H:M:S') + ' ' + str(row['Mag']),
                            fill_color=color, # divvy color
                           ).add_to(m)
    for index, row in top3.iterrows():
        subcat = catalog.loc[catalog['Reference']==row['Reference']]
        subcat.reset_index(drop=True, inplace=True)
        ind_max = subcat['MAD'].idxmax()
        folium.CircleMarker([subcat.iloc[ind_max]['latitude'], subcat.iloc[ind_max]['longitude']], popup=row['N'], fill_color='blue', radius = 20).add_to(m)

    fig, ax = plt.subplots(2, 1, figsize=(16, 4), sharex=True)
    markerlines, stemlines, _ = ax[0].stem(catalog['Date'], catalog['Mag'], 'o', linefmt='-', basefmt='black')
    plt.setp(stemlines, 'linewidth', 1)
    plt.setp(markerlines, 'markeredgecolor', 'black')

    for index, row in catalog.iterrows():
        if row['CC'] > 0.98:
            ax[0].plot(row['Date'], row['Mag'], 'o', color='red')
        else:
            ax[0].plot(row['Date'], row['Mag'], 'o', color='blue')
    ax[0].set_xlabel('Date')
    ax[0].set_ylabel('Magnitude')
    ax[0].set_title(u'Template Matching Catalog for MAD ≥' + str(mad))
    ax[0].grid(True)
    # plot colorcoded by magnitude and add colorbar
    #ax[1].scatter(catalog['Date'], catalog['Depth'], c=catalog['Mag'], s=10)
    cax = inset_axes(ax[1], width="2%", height="100%", loc='upper right', borderpad=0)
    scatter = ax[1].scatter(catalog['Date'], catalog['Depth'], c=catalog['Mag'], s=catalog['Mag']*30, cmap='hot_r',edgecolor='black')
    cbar = plt.colorbar(scatter, ax=ax[1],cax=cax)
    cbar.set_label('Magnitude')

    #ax[1].plot(catalog['Date'], catalog['Depth'], 'o', markersize=2)
    ax[1].set_xlabel('Date')
    ax[1].set_ylabel('Depth')
    ax[1].invert_yaxis()
    ax[1].grid(True)
    #ax[2].plot(catalog['Date'], catalog['MAD'], 'o', markersize=2)
    #ax[2].set_xlabel('Date')
    #ax[2].set_ylabel('CC')
    #ax[2].grid(True)
    #plt.tight_layout()
    plt.savefig(f'Figure_{config}.png', dpi=300)
    #m.show_in_browser()
    m.save(f'map_mad_{config}.html')  
