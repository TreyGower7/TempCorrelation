import numpy as np
import xarray as xr
import numpy.ma as ma

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

def adjust_nan_T(dp, T):
    """
    In order for the average in the temperature data to reflect the precipitation values I need to remove the indices that are nan in precipitation

    Args:

    Returns:
    a nan value adjusted dataset for temperature
    """
    zero_indices = np.where(dp == 0)
    T[zero_indices] = np.nan
    return T

def coarse_grain(ds):
    """
    Coarse-grain a multidimensional array by grouping values based on a specified factor.

    Args:
    Ds = a dataset, factor = the coarse graining factor 
    Returns:
    coarse_ds = the coarse-grained array
    """
    #In order for the average in the temperature data to reflect the precipitation values I need to remove the indices that are nan in precipitation
    m = len(ds)
    #The following line only works because I know I want my matrices to be 8x10 
    n = len(ds[0]-9)
#    for i in range(m)
    #Create the sub matrix and caluclate the mean for each
    for i in range(0,m,8):
        for j in range(0,n,10):
            sub_ds= ds[i:i+8, j:j+10]

            
    
    #average over the sub matrix ignoring masked values
    avg = ma.mean()
    return ds

path = '/corral/utexas/hurricane/tgower/har_dataset_02/Pot_Temp_HHar_d02.nc'
ds_T = xr.open_dataset(path)

path1 = '/corral/utexas/hurricane/tgower/har_dataset_02/Precipt_HHar_d02.nc'
ds_P = xr.open_dataset(path1)

Temp_ds = ds_T['T']

Precip_data = ds_P['RAIN_tot']
print("...Populating Subsets...")
print("_________________________________________________\n")
dp = find_dp(Precip_data)

dpnew = np.where(dp[3] == 0, np.nan, dp[3])
#Masking the Nan values for precipitation
mask_dp = ma.masked_invalid(dpnew)

Tnew = Temp_ds[3+12][0].values.flatten()
#zeroing out corresponding temperature values with nan
nan_T = adjust_nan_T(dp[3].values.flatten(), Tnew)
mask_T = ma.masked_invalid(nan_T)

print(mask_T)
coarse_dp = coarse_grain(mask_dp)
coarse_T = coarse_grain(mask_T)

#print("Original data:")
#print(len(Temp_ds))
#print(len(Temp_ds[0]))
#print(Temp_ds)
#print("\nCoarsened data:")
#print(len(coarsened_data))
#print(len(coarsened_data[0]))
#print(coarsened_data)

