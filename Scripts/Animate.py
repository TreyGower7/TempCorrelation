import PIL
import numpy as np
from PIL import Image
image_frames_T = []
image_frames_P = []
image_frames_Press = []


hours = 132

#Plots taken every 8 hours
for i in range(0,hours,6):
    new_frame_T = PIL.Image.open(r'/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Temp_plots/Temp_hr' + str(i) + '.0.jpg')
    image_frames_T.append(new_frame_T)

    new_frame_P = PIL.Image.open(r'/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Precip_plots/Precip_hr' + str(i) + '.0.jpg')
    image_frames_P.append(new_frame_P)
    
    new_frame_Press = PIL.Image.open(r'/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Press_plots/Press_hr' + str(i) + '.0.jpg')
    image_frames_Press.append(new_frame_Press)

image_frames_T[0].save('/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Temperature_Timelapse.gif', format = 'GIF',
        append_images = image_frames_T[1:],
        save_all =True, duration=350, 
        loop=0)

image_frames_P[0].save('/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Precip_Timelapse.gif', format = 'GIF',
        append_images = image_frames_P[1:],
        save_all =True, duration=350,
        loop=0)

image_frames_Press[0].save('/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Pressure_Timelapse.gif', format = 'GIF',
        append_images = image_frames_Press[1:],
        save_all =True, duration=350,
        loop=0)
