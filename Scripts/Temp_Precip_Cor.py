import numpy as np
import xarray as xr

"""
Caluclating Correlation Coefficients for Temperature and Precipitation data
(altitude is set constant at z = 0)
"""

__author__ = "Trey Gower"

def rm_zeros(dp,T):
    """ Removing zero values of precipitation and the corresponding temperature values

     Args: Precipitation and temperature at time t = i for every 3 hour time step

     Returns: Two new adjusted numpy arrays excluding zero values of precipitation

    """
    #using numpy optimized algorithm to get the indices of the zeros
    #for i in range(len(dp)):
    zero_indices = np.where(dp == 0)
    new_dp = np.delete(dp, zero_indices)
    new_T = np.delete(T, zero_indices)
    
    return new_dp, new_T 

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
   
#def mean(values):
#    return sum(values) / len(values)

#calculate the correlation coefficient (This works but is less optimal)
#def ccf(T, dp):
       
#    x_mean = mean(T)
#    y_mean = mean(dp)

#    numer = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(T, dp))
#    denom_T = sum((xi - x_mean)**2 for xi in T)
#    denom_dp = sum((yi - y_mean)**2 for yi in dp)

#    correlation = numer / np.sqrt(denom_T * denom_dp)

#    return correlation

def txt_w(ctp):
    f = open(f'Correlation_Coefficients.txt','w')
    for i in range(1,len(ctp),1):
        f.write(f't (hours) = {i*3}: Correlation Coefficient = {ctp[i]}\n\n')
    f.close()

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
    for i in range(len(dp)):
        if i != 0:
            print('...Removing zeros for t = ' + str(i*3) + 'hrs...')
            dpnew, Tnew = rm_zeros(dp[i].values.flatten(),Temp_data[i+12][0].values.flatten())
            ctp.append(np.corrcoef(Tnew,dpnew)[0,1])
        else:
            continue

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




