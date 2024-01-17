import numpy as np
import xarray as xr
import numpy.ma as ma
import json
"""
Calculating Correlation Coefficients for Temperature and Precipitation data
(altitude is set constant at z = 0)
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
        if i >=0:
            dp.append(Precip_ds[i]-Precip_ds[i-12])

    # Convert the list of differences to an xarray DataArray
    dp_xr = xr.concat(dp, dim='time')
    return dp_xr
   
def txt_w(ctp, state):
    coeffs = []
    for i in range(1,len(ctp),1):
        coeffs.append({'Time(hrs)': i*3, 'Correlation Coefficient': ctp[i]})
    
    if state == 1:
        with open('/corral/utexas/hurricane/tgower/TempCorrelation/Corr_Coeffs_har_02/Correlation_Coeffs_Coarse.json','w') as json_file:
            json.dump(coeffs, json_file, indent=2)
    else:
        with open('/corral/utexas/hurricane/tgower/TempCorrelation/Corr_Coeffs_har_02/Correlation_Coeffs.json','w') as json_file:
            json.dump(coeffs, json_file, indent=2)
    
    return 'Coefficients saved to Correlation_Coefficients text files'
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

        if i == 0:
            sub_ds= ds[0:8, 0:10]
            mask_ds= ma.masked_invalid(sub_ds)
        j +=2
        coarse_avg[i//8] = ma.mean(mask_ds)
    return coarse_avg

def main():

    path = '/corral/utexas/hurricane/tgower/har_dataset_02/Pot_Temp_HHar_d02.nc'
    ds_T = xr.open_dataset(path)

    path1 = '/corral/utexas/hurricane/tgower/har_dataset_02/Precipt_HHar_d02.nc'
    ds_P = xr.open_dataset(path1)

# Access a specific variable
    print("\n...Getting Temperature and Precipitation Data...")
    print("_________________________________________________\n")

# Get Data
    Temp_data = ds_T['T']
    Precip_data = ds_P['RAIN_tot']
    print("...Populating Subsets...")
    print("_________________________________________________\n")
    dp = find_dp(Precip_data)    

    variable_names_P = ds_P.keys()
    variable_names_T = ds_T.keys()

#Key information
    print("\nKey Names: ")
    print(str(variable_names_P) + "\n")
    print("\nKey Names: ")
    print(str(variable_names_T) + "\n")


# Correlation
    print("...Finding Correlation Coefficient for each 3 hour time step...")
    print("_________________________________________________\n")
    
    ctp = []
    ctp_coarse = []
    print(len(Temp_data))
    for i in range(len(dp)):
        #Skip time step t = 0
        print('...Calculating t = ' + str(i*3) + 'hrs...')
        dpnew = np.where(dp[i] == 0, np.nan, dp[i])
        #Masking the Nan values for precipitation
        mask_dp = ma.masked_invalid(dpnew)

        Tnew = Temp_data[i*12][0].values.flatten()
        
        #Calculate non-coarse grained correlation
        ctp.append(ma.corrcoef(Tnew,mask_dp.flatten())[0,1])

        #Extra step #zeroing out corresponding temperature values with nan for coarse graining
        nan_T = adjust_nan_T(dp[i].values.flatten(), Tnew)

        #revert Temp back to 2d for coarse graining
        nan_T = nan_T.reshape(Temp_data[i*12][0].shape)
        
        #Calculate Coarse grained averages for sub matrices (masking doesnt occur until function coarse_grain is called here)
        coarse_dp = coarse_grain(dpnew)
        coarse_T = coarse_grain(nan_T)
        

        #Mask averages that are close to zero
        coarse_dp = np.where(coarse_dp == 0, np.nan, coarse_dp)
        coarse_T = np.where(coarse_T == 0, np.nan, coarse_T)
        
        
        #Masking nan values
        mask_cdp = ma.masked_invalid(coarse_dp)
        mask_cT = ma.masked_invalid(coarse_T)
        
        ctp_coarse.append(ma.corrcoef(mask_cT.flatten(),mask_cdp.flatten())[0,1])
    
# Write outputs to text file
    txt_w(ctp,0)
    txt_w(ctp_coarse, 1)

    #close datasets
    ds_T.close()
    ds_P.close()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
