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

original_array = np.array([1, 0, 2, 0, 3, 0, 4])

fn = '/corral/utexas/hurricane/tgower/har_dataset_02/Precipt_HHar_d02.nc'
dataset = xr.open_dataset(fn)
ds = dataset['RAIN_tot'][48]

# Replace zero values with NaN
ds_no_zeros = ds.where(ds != 0)

# Perform calculations on the modified dataset
result = ds_no_zeros.mean(dim=('p','r'))  # Replace 'your_variable' with the variable you're interested in

# Display the original dataset, the modified dataset, and the result
print("Original Dataset:")
print(ds)

print("\nModified Dataset (Zeros replaced with NaN):")
#print(ds_no_zeros)

print("\nResult of calculations excluding zeros:")
print(result)

m = mean(ds)
print(m)
