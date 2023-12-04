import numpy as np
import xarray as xr

ind = 20
def mean(dp):
    result = 0
    L = 0
    for i in range(len(dp)):
        for j in range(len(dp[i])):
            if dp[i][j].values !=0:
                result += dp[i][j].values
                L += 1
    mean = result/L
    return mean

def rm_zeros(dp):
    """ Removing zero values of precipitation and the corresponding temperature values

     Args: Precipitation and temperature at time t = i for every 3 hour time step

     Returns: Two new adjusted numpy arrays excluding zero values of precipitation

    """
    
    #using numpy optimized algorithm to get the indices of the zeros
    zero_indices = np.where(dp[i] == 0)
    new_dp = np.delete(dp[i], zero_indices)

        #np.concatenate(new_dp, dp[i])
   #    ndp.append(new_dp)
         #dpn = xr.concat(new_dp) 
   # ndp = xr.DataArray(ndp, dims=('p', 'r'))

    return dp


fn = '/corral/utexas/hurricane/tgower/har_dataset_02/Precipt_HHar_d02.nc'
dataset = xr.open_dataset(fn)
ds = dataset['RAIN_tot'][48]

dp = ds.values.flatten()
print(len(dp))
zero_indices = np.where(dp == 0)
new_dp = np.delete(dp, zero_indices)
print(len(new_dp))

#newdp =  rm_zeros(ds)

#print(newdp)

#m = mean(ds)
#print(m)
