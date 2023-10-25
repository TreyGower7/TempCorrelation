import PIL
import numpy as np
from PIL import Image
image_frames = []

hours = 64

#Plots taken every 8 hours
for i in range(0,hours,8):
    new_frame = PIL.Image.open(r'/corral/utexas/hurricane/tgower/TempCorrelation/Plots/Temp_hr' + str(i) + '.0.jpg')
    image_frames.append(new_frame)

image_frames[0].save('Temperature_Timelapse.gif', format = 'GIF',
        append_images = image_frames[1:],
        save_all =True, duration=350, 
        loop=0)
