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
        return ctp
    except:
        return 'failed to retrieve coefficients'

def create_plot(coeff, time):
    """ Takes in coefficients and times and generates scatter plots
     
     Args: Coeffs, Time
     
     Returns: Scatter Plot
    """
    #plotting coefficients vs time

    plt.scatter(time, coeff, label='Coeffs')
    
    #trendline 
    fit = np.polyfit(time, coeff, 1)
    fit_fn = np.poly1d(fit)
    
    plt.plot(coeff,fit_fn(coeff),color='red', label='Trendline')
    plt.legend()

    plt.xlabel('Time (hrs)')
    plt.ylabel('Coefficients')
    plt.title('Non-coarse Coefficient Scatter')
    plt.savefig('/corral/utexas/hurricane/tgower/TempCorrelation/Corr_Coeffs_har_02/NC_Scatter')
    
    print('Plot Generated')

def main():
    """ Main function """

    ctp = get_ctp()
    time_steps = len(ctp)
    coeff = np.zeros([time_steps, 1])
    time = np.zeros([time_steps, 1])
    
    for i in range(time_steps):
        coeff[i] = ctp[i]['Correlation Coefficient']
        time[i] = ctp[i]['Time(hrs)']
    
    #Generate Plot
    create_plot(time.flatten(), coeff.flatten())

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
