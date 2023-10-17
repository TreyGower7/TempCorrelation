import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

fn = '/corral/utexas/hurricane/tgower/har_dataset_02/Pot_Temp_HHar_d02.nc'
dataset = nc.Dataset(fn)

# Get the variable names
variable_names = dataset.variables.keys()

#Key information
print("\nKey Names: ")
print(str(variable_names) + "\n")
print("Times taken with a step size of 15 seconds\n")
print("------------------------------------------\n")

# Access a specific variable
print("...Getting Latitudinal and Longitudinal Data...\n")
temp_var = dataset.variables['T']
lon = dataset.variables['x'][:]
lat = dataset.variables['y'][:]
z = dataset.variables['z'][:]
time_data = dataset.variables['time']

#Temp data at time t=0
im_data = temp_var[0]

#close dataset
dataset.close()

print("...Generating Plot...\n")
# Create a Plate Carrée projection
projection = ccrs.PlateCarree()

# Create a plot with the specified projection
fig, ax = plt.subplots(subplot_kw={'projection': projection})

# Assuming lon and lat are defined
im_extent = (lon.min(), lon.max(), lat.min(), lat.max())

# Display the single slice
mp = ax.imshow(im_data[0], extent=im_extent, cmap='jet', origin='lower')

# adding colorbar and adjust the size
cbar = fig.colorbar(mp, ax=ax)
cbar.minorticks_on()

#additional feeatures from Cartopy
states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none')
ax.add_feature(cfeature.BORDERS,edgecolor='blue')
ax.add_feature(states_provinces, edgecolor='blue')
ax.add_feature(cfeature.COASTLINE)

#adding the long lat grids and enabling the tick labels
gl = ax.gridlines(draw_labels=True,alpha=0.1)
gl.top_labels = False
gl.right_labels = False


# Set plot title and labels
plt.title('Temperature Data')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

#Save figure
plt.savefig("Temp_test.jpg",dpi=330)
print('Plot Generated\n')
