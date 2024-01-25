import numpy as np 
import matplotlib.pyplot as plt
import json

"""
Python script to generate scatter plots of my correlation coefficients plotting 
Correlation vs time
"""

__author__ = "Trey Gower"

def get_ctp():
    """ Takes in correlation text file and makes it readable
     Args: None
     Returns: Calculated coefficients for each time step
    """
    try:
        with open('/corral/utexas/hurricane/tgower/TempCorrelation/Corr_Coeffs_har_02/Correlation_Coeffs.json','r') as f:
            ctp = json.load(f)
        with open('/corral/utexas/hurricane/tgower/TempCorrelation/Corr_Coeffs_har_02/Correlation_Coeffs_Coarse.json','r') as f:
            ctp_coarse = json.load(f)
        return ctp, ctp_coarse
    except:
        return 'failed to retrieve coefficients'

def high_low(coeff, time):
    """ Takes in coefficients and times and generates high and low subsets

     Args: Coeffs, Time

     Returns: high and low subsets
    """
    high = []
    low = []
    t_low = []
    t_high = []

    for i in range(len(coeff)):
        if abs(float(coeff[i])) >= .3:
            high.append(coeff[i])
            t_high.append(time[i])
        else:
            low.append(coeff[i])
            t_low.append(time[i])
    
    return high, t_high, low, t_low

def create_plot(coeff, time, coeff_coarse, time_coarse):
    """ Takes in coefficients and times and generates scatter plots
     
     Args: Coeffs, Time
     
     Returns: Scatter Plot
    """
    High, t_high, Low, t_low = high_low(coeff, time)
    High_coarse, t_high_coarse, Low_coarse, t_low_coarse = high_low(coeff_coarse, time_coarse)

    #plt.scatter(t_high, High, marker='o', facecolors='none', edgecolors='r', label = 'High Correlation')
    #plt.show()
    #plt.scatter(t_low, Low, marker='o', facecolors='none', edgecolors='b', label = 'Low Correlation')
    #plt.show()
    #plt.scatter(t_high_coarse, High_coarse, color='pink', marker = 'v', label = 'Coarse High Correlation')
    #plt.show()
    #plt.scatter(t_low_coarse, Low_coarse, color='green', marker = 'v', label = 'Coarse Low Correlation')
    
    cbar, ax = plt.subplots()
    points = ax.scatter(time, coeff, c=coeff,label='Non-Coarse Correlation', cmap = 'rainbow')
    cb1 = cbar.colorbar(points, label = 'Non-Coarse')
    cb1.ax.invert_yaxis()
    plt.show()

    points = ax.scatter(time_coarse, coeff_coarse, c=coeff_coarse,label='Coarse Correlation', cmap = 'plasma',edgecolors = 'k',linewidth = .5, marker = 'v', s =10)
    cb = cbar.colorbar(points, label = 'Coarse')
    cb.ax.invert_yaxis()
    
    plt.legend() 
    plt.gca().invert_yaxis()
    plt.xlabel('Time (hrs)')
    plt.ylabel('Coefficients')
    plt.title('Coarse/Non-Coarse Coefficient Scatter')
    
    plt.show()
    plt.savefig('/corral/utexas/hurricane/tgower/TempCorrelation/Corr_Coeffs_har_02/NC_Scatter')
    
    print('Plot Generated')

def main():
    """ Main function """

    ctp, ctp_coarse = get_ctp()
    time_steps = len(ctp)
    coeff = np.zeros([time_steps])
    time = np.zeros([time_steps])
    
    coeff_coarse = np.zeros([time_steps])
    time_coarse = np.zeros([time_steps])

    for i in range(time_steps):
        coeff[i] = ctp[i]['Correlation Coefficient']
        time[i] = ctp[i]['Time(hrs)']
        
        coeff_coarse[i] = ctp_coarse[i]['Correlation Coefficient']
        time_coarse[i] = ctp_coarse[i]['Time(hrs)']
    
    #Generate Plot
    create_plot(coeff, time, coeff_coarse, time_coarse)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
