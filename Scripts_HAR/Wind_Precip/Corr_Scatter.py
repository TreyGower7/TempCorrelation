import numpy as np 
import matplotlib.pyplot as plt
import json
import matplotlib.lines as mlines

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
        with open('/corral/utexas/hurricane/tgower/TempCorrelation/Corr_Coeffs_har_02/Wind_Precip/Correlation_Coeffs.json','r') as f:
            ctp = json.load(f)
        with open('/corral/utexas/hurricane/tgower/TempCorrelation/Corr_Coeffs_har_02/Wind_Precip/Correlation_Coeffs_Coarse.json','r') as f:
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
    
    #Hgh Res plot
    cbar, ax = plt.subplots()
    points = ax.scatter(time, coeff, c=coeff, cmap = 'plasma', s=100)
    
    plt.show()
    #Coarse Plot
    points = ax.scatter(time_coarse, coeff_coarse, c=coeff_coarse, cmap = 'plasma',edgecolors = 'k',linewidth = .7, marker = 'v', s =100)
    cb = cbar.colorbar(points)
    cb.ax.invert_yaxis()
    
    #Legend settings
    Coarse_leg = mlines.Line2D([], [], color='black', marker='v',
                          markersize=7.5, label='Coarse-grained data', fillstyle='none')
    Highres_leg = mlines.Line2D([], [], color='black', marker='o',
                          markersize=7.5, label='High-resolution data', fillstyle='none')
    
    ax.legend(handles=[Highres_leg,Coarse_leg],handlelength=0, handleheight=0)

    #Vertical lines
    vertical_lines_x = [28, 75]
    for x_value in vertical_lines_x:
        plt.axvline(x=x_value, color='k', linestyle='--')

    #plt.gca().invert_yaxis()
    plt.xlabel('time (hrs)')
    plt.ylabel('Correlation coefficient')
    
    plt.show()
    plt.savefig('/corral/utexas/hurricane/tgower/TempCorrelation/Corr_Coeffs_har_02/Wind_Precip/NC_Scatter')
    
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
