import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def rm_zero(dp):
    for i in range(len(dp)):
        #print(len(dp[i]))
     #   for j in range(len(dp[i])):
    #temp = np.asarray(dp[1])
    #print(temp)
    #temp = temp[~np.all(temp == 0, axis = 1)]
    return temp
#Need to remove 0s from precipitation data and somehow match temp and precip data
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

def main():

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
    lon = dataset['x'][:]
    lat = dataset['y'][:]

    dp = find_dp(Precip_data)
    print(dp[0][0].values)

    dp = rm_zero(dp)

    #print(lat[0][400].values)
    print(dp[0])
#close dataset
    dataset.close()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

