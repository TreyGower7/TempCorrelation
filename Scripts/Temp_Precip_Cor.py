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
        if i >=0 && Precip_ds[i].values != 0:
            dp.append(Precip_ds[i]-Precip_ds[i-12])

    # Convert the list of differences to an xarray DataArray
    dp_xr = xr.concat(dp, dim='time')
    return dp_xr
   
def mean(values):
    return sum(values) / len(values)

#calculate the correlation coefficient
def ccf(T, dp):
    
    #To account for the zeros in precipitation and to ensure indices between Temp and Precipitation are uniform we can calculate
    #the mean for temp and precipitation with the same for loops to ensure wherever Precipitation is zero the temperature value at that point 
    #is not getting added into the equation

    x_mean = mean(T)
    y_mean = mean(dp)

    numer = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(T, dp))
    denom_T = sum((xi - x_mean)**2 for xi in T)
    denom_dp = sum((yi - y_mean)**2 for yi in dp)

    correlation = numer / np.sqrt(denom_T * denom_dp)

    return correlation

def txt_w(ctp,num):
    f = open(f'Correlation_Coefficients{num}.txt','w')
    for i in range(len(ctp)):
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
    
    print(Temp_data[0][0].dims)
    print(dp[0].dims)
# Correlation
    print("...Finding Correlation Coefficient for each 3 hour time step...")
    print("_________________________________________________\n")
    
    ctp = []
    for i in range(len(dp)):
        if i != 0:
            ctp.append(np.corrcoef(Temp_data[i+12][0].values.flatten(),dp[i].values.flatten())[0,1])
        else:
            ctp.append(np.corrcoef(Temp_data[0][0].values.flatten(),dp[i].values.flatten())[0,1])
    
    ctp2 = []
    for i in range(len(dp)):
        if i != 0:
            ctp2.append(ccf(Temp_data[i+12][0].values.flatten(),dp[i].values.flatten()))
        else:
            ctp2.append(ccf(Temp_data[0][0].values.flatten(),dp[0].values.flatten()))

# Write outputs to text file
    txt_w(ctp,1)
    txt_w(ctp2,2)
    txt_w(ctp3,3)

    #print correlation at each 3 hour time step
    print('Coefficients saved to Correlation_Coefficients text files')
    #close datasets
    ds_T.close()
    ds_P.close()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()



