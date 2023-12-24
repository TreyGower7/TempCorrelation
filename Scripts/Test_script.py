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
    Ds = a dataset where the nan values are not yet masked 
    Returns:
    coarse_avg = the coarse grained averages
    """
    coarse_avg = np.zeros((66,1))
    #In order for the average in the temperature data to reflect the precipitation values I need to remove the indices that are nan in precipitation
    #The following two lines only work because I know I want my matrices to be 8x10 (I am intentionally excluding the last 6 hours)
    m = len(ds)-24
    n = len(ds[0])-9
    
    j = 0
    #Create the sub matrix and caluclate the mean for each
    for i in range(0,m,8):
        #Need j to increment by 2 in order for our second index to reach 660
        if i != 0:
            #Must increment i value by 1 as to not include the previous index
            sub_ds= ds[(i+1):i+8, (i+j)+1:(i+j)+10] 
            
            mask_ds= ma.masked_invalid(sub_ds)
            coarse_avg[i//8] = ma.mean(mask_ds)
        
        if i == 0:
            sub_ds= ds[0:8, 0:10]
            
            mask_ds= ma.masked_invalid(sub_ds)
            coarse_avg[i//8] = ma.mean(mask_ds)
        j +=2

        #average the values in the submatrix and store
    return coarse_avg

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
Tnew = Temp_ds[3*12][0].values.flatten()
#zeroing out corresponding temperature values with nan
nan_T = adjust_nan_T(dp[3].values.flatten(), Tnew)
bruh = nan_T.reshape(Temp_ds[3*12][0].shape)

coarse_dp = coarse_grain(dpnew)
coarse_T = coarse_grain(bruh)

print(coarse_dp)
