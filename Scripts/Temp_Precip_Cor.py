import numpy as np
import xarray as xr

"""
Caluclating Correlation Coefficients for Temperature and Precipitation data
(altitude is set constant at z = 0)
"""

__author__ = "Trey Gower"

def get_Data():
    """ Retrieve Netcdf data

     Args: t to acces a specific time and z to acces a specific altitude

     Returns: List containing 2 indices of the Temp and Precip data

    """
    path = '/corral/utexas/hurricane/tgower/har_dataset_02/Pot_Temp_HHar_d02.nc'
    ds_T = xr.open_dataset(path)

    path1 = '/corral/utexas/hurricane/tgower/har_dataset_02/Precipt_HHar_d02.nc'
    ds_P = xr.open_dataset(path1)

    # Access a specific variable
    print("...Getting Temperature and Precipitation Data...\n")
    print("_________________________________________________\n")

    #Get Data
    temp_data = ds_T['T']
    precip_data = ds_P['RAIN_tot']
    
    return [Temp_ds, Precip_ds]

def correlation_coeff(t,T,P):
  """ Calculate correlation between Temperature and Precipitation

     Args: t(List containing two values) to acces a specific time range, Temperature dataset, and precipitation dataset

     Returns: List containing correlation coefficients for the full set and sliced sets

    """
    if type(t) != list:
        #setting default t to whole dataset for any parameter that is not a input range
        t = [1,528]
    #calculate dp using pressure data \(\lamda)
    for i in range(t[0],t[1],1):
        #Calculate Correlation
        
        Ctp =

def main():
    """ Main entry point """
    print("hello world")
    
    data = get_data()

    correlation = correlation_coeff()
    
    #close datasets
    ds_T.close()
    ds_P.close()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

