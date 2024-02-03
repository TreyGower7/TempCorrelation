import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def find_dp(Precip_ds):
    """ Calculate change in Precipitation data for every 3 hour time step

     Args: Precipitation dataset

     Returns: The change in precipitation from Precip_ds(i)-Precip_ds(i-12)

    """
    dp = []
    #index by 12 for data every 3 hours
    for i in range(0,528,12):
        if i >=0:
            dp.append(Precip_ds[i]-Precip_ds[i-12])

    # Convert the list of differences to an xarray DataArray
    dp_xr = xr.concat(dp, dim='time')
    return dp_xr

fn = '/corral/utexas/hurricane/tgower/har_dataset_02/Precipt_HHar_d02.nc'
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
Precip_data = dataset['RAIN_tot']
time = dataset['time'][:]
lon = dataset['x'][:]
lat = dataset['y'][:]
hours = len(time)

#Finding change in precipitation every 3 hours
dp = find_dp(Precip_data)

print("...Generating Plots...")

#graphing change in precipitation every 3 hours
for i in range(len(dp)):
    # Create a Plate Carrée projection
    projection = ccrs.PlateCarree()

    # Create a plot with the specified projection

    fig, ax = plt.subplots(subplot_kw={'projection': projection})
    
    im_data = dp[i]
        # Assuming lon and lat are defined
    im_extent = (lon.min(), lon.max(), lat.min(), lat.max())

        #Display the single slice
    mp = ax.imshow(im_data, extent=im_extent, cmap='jet', origin='lower')

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
    cbar.set_label('milimeters (mm)', rotation = -90, labelpad = 12)
    cbar.minorticks_on()
    plt.title('Precipitation Data at t= '+ str(i*3) +' Hours')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

#Save figure and clear previous
    plt.savefig("/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Precip_plots/Precip_hr" + str(i*3) + ".jpg",dpi=330)
    plt.clf()
#close dataset
dataset.close()
print('Plots Generated\n')
