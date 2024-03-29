import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

fn = '/corral/utexas/hurricane/tgower/ida_dataset_02/Pressu_HIda_d02.nc'
dataset = xr.open_dataset(fn)

# Get the variable names
variable_names = dataset.keys()

#Key information
print("\nKey Names: ")
print(str(variable_names) + "\n")
print("Times taken with a step size of 15 mins\n")
print("------------------------------------------\n")

# Access a specific variable
print("...Getting Latitudinal and Longitudinal Data...\n")
Press_var = dataset['P']
time = dataset['time'][:]
lon = dataset['x'][:]
lat = dataset['y'][:]
hours = len(time)
print("...Generating Plots...")

#increment by 12 in order to plot data for every 3 hours
for i in range(0,312,12):
    # Create a Plate Carrée projection
    projection = ccrs.PlateCarree()

    # Create a plot with the specified projection

    fig, ax = plt.subplots(subplot_kw={'projection': projection})
    
    im_data_z15 = Press_var[i]
        # Assuming lon and lat are defined
    im_extent = (lon.min(), lon.max(), lat.min(), lat.max())

        #Display the single slice fro z=15
    mp = ax.imshow(im_data_z15[15], extent=im_extent, cmap='jet', origin='lower')

    #additional features from Cartopy
    states_provinces = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='10m',
            facecolor='none')
    ax.add_feature(cfeature.BORDERS,edgecolor='blue')
    ax.add_feature(states_provinces, edgecolor='blue')
    ax.add_feature(cfeature.COASTLINE)

#adding the long lat grids and enabling the tick labels
    gl = ax.gridlines(draw_labels=True,alpha=0.1)
    gl.top_labels = False
    gl.right_labels = False
    # Set plot title and labels
 # adding colorbar and adjust the size
    cbar = fig.colorbar(mp, ax=ax)
    cbar.set_label('Pascals (Pa)', rotation = -90, labelpad = 12)
    cbar.minorticks_on()
    plt.title('Pressure Data at t= '+ str((i*15)/60) +' Hours')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

#Save figure and clear previous
    plt.savefig("/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Plot_IDA_02/Press_plots/Press_hr" + str((i*15)/60) + ".jpg",dpi=330)
    plt.clf()
#close dataset
dataset.close()
print('Plots Generated\n')
