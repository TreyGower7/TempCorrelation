import numpy as np
import xarray as xr

"""
Caluclating Correlation Coefficients for Temperature and Precipitation data
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


def correlation_coeff(t,T,dP):
  """ Calculate correlation between Temperature and Precipitation

     Args: t(List containing two values) to acces a specific time range, Temperature dataset, and precipitation dataset

     Returns: List containing correlation coefficients for the full set and sliced sets

    """
    #adjust for time values given
    if type(t) != list:
        #setting default t to whole dataset for any parameter that is not an input range
        t = [1,43]

    #Updated every 3 hours
    for i in range(t[0],t[1]),1):
        #Calculate Correlation
        
        CTP = np.dot(T,dP) / np.sqrt(np.dot(T,T)*np.dot(dP,dP)) 
    return CTP

def main():

    path = '/corral/utexas/hurricane/tgower/har_dataset_02/Pot_Temp_HHar_d02.nc'
    ds_T = xr.open_dataset(path)

    path1 = '/corral/utexas/hurricane/tgower/har_dataset_02/Precipt_HHar_d02.nc'
    ds_P = xr.open_dataset(path1)

    # Access a specific variable
    print("\n...Getting Temperature and Precipitation Data...")
    print("_________________________________________________\n")

    #Get Data
    Temp_data = ds_T['T']
    Precip_data = ds_P['RAIN_tot']
    print("...Populating Subsets...")
    print("_________________________________________________\n")
    dp = find_dp(Precip_data)    
   
    #Subset of the Temperature Data
    #T_sub = []
    #index by 12 for data every 3 hours
    #for i in range(0,528,12):
    #    T_sub.append(Temp_data[i])

    # Convert the list of differences to an xarray DataArray
    #T_xr = xr.concat(T_sub, dim='time')

    print(T_xr)
    print(dp)
# Correlation
    print("...Finding Correlation Coefficient for each 3 hour time step...")
    print("_________________________________________________\n")
    correlation = correlation_coeff(0,Temp_data,dp)
    
    #print correlation at each 3 hour time step
    for i in range(len(correlation)):
        print('Correlation for t = ' + str(i*3) + ': ' + correlation[i] + '\n')

    #close datasets
    ds_T.close()
    ds_P.close()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

