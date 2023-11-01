import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


"""
Caluclating Correlation Coefficients for Temperature and Precipitation data
(altitude is set constant at z = 15)
"""

__author__ = "Trey Gower"

def find_dp(Precip_ds):
    """ Calculate change in Precipitation data for every 3 hour time step

     Args: Precipitation dataset

     Returns: The change in precipitation from Precip_ds(i)-Precip_ds(i-12)

    """
    dp = []
    #index by 12 for data every 3 hours
    for i in range(0,528,12):
        #saving our data into a xr dataarray for more efficiency
        dp.append(Precip_ds[i]-Precip_ds[i-12])
    # Convert the list of differences to an xarray DataArray
    dp_xr = xr.concat(dp, dim='time')
    return dp_xr

def main():

    path = '/corral/utexas/hurricane/tgower/har_dataset_02/Pot_Temp_HHar_d02.nc'
    ds_T = xr.open_dataset(path)

    path1 = '/corral/utexas/hurricane/tgower/har_dataset_02/Precipt_HHar_d02.nc'
    ds_P = xr.open_dataset(path1)

    # Access a specific variable
    print("...Getting Temperature and Precipitation Data...\n")
    print("_________________________________________________\n")
    Temp_data = ds_T['T']
    Precip_data = ds_P['RAIN_tot']  
    time = ds_P['time'][:]
    lon = ds_P['x'][:]
    lat = ds_P['y'][:]
    hours = len(time)
    dp = find_dp(Precip_data)    
    
    # Create a Plate Carrée projection
    projection = ccrs.PlateCarree()

    # Create a plot with the specified projection

    fig, ax = plt.subplots(subplot_kw={'projection': projection})
    
    im_data = dp[5]
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
    cbar.set_label('milimeters (mm)', rotation = -90, labelpad=12)
    cbar.minorticks_on()
    plt.title('Precipitation Data at t= 0 Hours')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

#Save figure and clear previous
    plt.savefig("DPrecip_test.jpg",dpi=330)
    plt.clf()
#close dataset
    ds_T.close()
    ds_P.close()
    print('Plots Generated\n')

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

