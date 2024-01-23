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
        with open('/corral/utexas/hurricane/tgower/TempCorrelation/Corr_Coeffs_IDA_02/Correlation_Coeffs.json','r') as f:
            ctp = json.load(f)
        return ctp
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

def create_plot(coeff, time):
    """ Takes in coefficients and times and generates scatter plots
     
     Args: Coeffs, Time
     
     Returns: Scatter Plot
    """
    High, t_high, Low, t_low = high_low(coeff, time)

    plt.scatter(t_high, High, color='red', label = 'High Correlation')
    plt.show()
    plt.scatter(t_low, Low, color='blue', label = 'Low Correlation')
    
    plt.legend()

    plt.xlabel('Time (hrs)')
    plt.ylabel('Coefficients')
    plt.title('Coarse/Non-Coarse Coefficient Scatter')
    
    plt.show()
    plt.savefig('/corral/utexas/hurricane/tgower/TempCorrelation/Corr_Coeffs_IDA_02/NC_Scatter')
    
    print('Plot Generated')

def main():
    """ Main function """

    ctp = get_ctp()
    time_steps = len(ctp)
    coeff = np.zeros([time_steps])
    time = np.zeros([time_steps])
    
    for i in range(time_steps):
        coeff[i] = ctp[i]['Correlation Coefficient']
        time[i] = ctp[i]['Time(hrs)']
    
    #Generate Plot
    create_plot(coeff, time)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
