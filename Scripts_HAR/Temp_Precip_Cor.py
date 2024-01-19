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
    sub_mat = the list of numpy sub matrices
    """
    # Get the dimensions
    rows, cols = ds.shape

    # Define size for sub matrices
    sub_mat_rows = 8
    sub_mat_cols = 10

    # Calculate sub-matrices in each dimension
    num_sub_mat_rows = rows // sub_mat_rows # Using floor division for zero remainder
    num_sub_mat_cols = cols // sub_mat_cols # Using floor division for zero remainder

    # Initialize list to store all sub matrices 
    sub_mats = []

    # Iterate through rows
    for i in range(num_sub_mat_rows):
        # Iterate through columns
        for j in range(num_sub_mat_cols):
            # Extracting each sub matrix
            sub_mat = ds[i * sub_mat_rows: (i + 1) * sub_mat_rows,
                               j * sub_mat_cols: (j + 1) * sub_mat_cols]
            # Append the sub matrix to the list
            sub_mats.append(sub_mat)

    return sub_mats

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
