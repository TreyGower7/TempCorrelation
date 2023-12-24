import numpy as np
import xarray as xr
import numpy.ma as ma

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
   
def txt_w(ctp):
    f = open(f'Correlation_Coefficients.txt','w')
    for i in range(1,len(ctp),1):
        f.write(f't (hours) = {i*3}: Correlation Coefficient = {ctp[i]}\n\n')
    f.close()

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
        #zeroing out corresponding temperature values with nan
        nan_T = adjust_nan_T(dp[i].values.flatten(), Tnew) 
        mask_T = ma.masked_invalid(nan_T)
        
        ctp.append(ma.corrcoef(Tnew,mask_dp.flatten())[0,1])

# Write outputs to text file
    txt_w(ctp)

    #print correlation at each 3 hour time step
    print('Coefficients saved to Correlation_Coefficients.txt file')
    #close datasets
    ds_T.close()
    ds_P.close()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()




