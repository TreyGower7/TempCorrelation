import PIL
import numpy as np
from PIL import Image
image_frames_T = []
image_frames_P = []
image_frames_Press = []


hours = 78

#Plots taken every 8 hours
for i in range(0,hours,3):
    new_frame_T = PIL.Image.open(r'/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Plot_IDA_02/Temp_plots/Temp_hr' + str(i) + '.0.jpg')
    image_frames_T.append(new_frame_T)

    new_frame_P = PIL.Image.open(r'/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Plot_IDA_02/Precip_plots/Precip_hr' + str(i) + '.jpg')
    image_frames_P.append(new_frame_P)
    
    new_frame_Press = PIL.Image.open(r'/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Plot_IDA_02/Press_plots/Press_hr' + str(i) + '.0.jpg')
    image_frames_Press.append(new_frame_Press)

image_frames_T[0].save('/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Plot_IDA_02/Temperature_Timelapse.gif', format = 'GIF',
        append_images = image_frames_T[1:],
        save_all =True, duration=350, 
        loop=0)

image_frames_P[0].save('/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Plot_IDA_02/Precip_Timelapse.gif', format = 'GIF',
        append_images = image_frames_P[1:],
        save_all =True, duration=350,
        loop=0)

image_frames_Press[0].save('/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Plot_IDA_02/Pressure_Timelapse.gif', format = 'GIF',
        append_images = image_frames_Press[1:],
        save_all =True, duration=350,
        loop=0)
