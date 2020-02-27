import os
import subprocess
import sys

PATH_TO_BLENDER = ''
# depth map scale, units in the generated depth map for RGB-D - 16-bit png
#DMP = 1   # 1 m - range 0-65535 m
DMP = 0.1 # 10 cm - range 0-6553.5 m
#DMP = 0.01 # 1 cm  - range 0-655.35 m
#DMP = 0.001 # 1 mm  - range 0-65.535 m

model_input_folder = "input"
model_output_folder = "output"

fpaths = []

try:
    model_input_folder = sys.argv[1]
except IndexError:
    # default value will be used
    pass

try:
    DMP = float(sys.argv[2])
except IndexError:
    # default value will be used
    pass

for rs,ds,_ in os.walk(model_input_folder):
    for d in ds:
        for rss,_,fss in os.walk(os.path.join(rs,d)):
            for f in fss:
                if f.endswith('obj'):
                    fpaths.append(os.path.join(rss,f))

filelist = ','.join(fpaths)

# this will run by Blender's bundled python
subprocess.run(os.path.join(PATH_TO_BLENDER,'blender')+" -b -P blender_generate_image_and_depth.py -- "+filelist, shell=True)

print("All RGB-Ds generated")

import exr2png as e2p
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

resoluton = ""
if DMP>=1:
    resolution = str(int(DMP))+"m"
elif DMP>=0.01:
    resolution = str(int(DMP*100))+"cm"
elif DMP>=0.001:
    resolution = str(int(DMP*1000))+"mm"

print("Depth maps will be scaled to "+resolution+" resolution covering range from 0 to "+str(DMP*65535)+" meters")

for fpath in fpaths:

    model_name = fpath.split('/')[-1][:-4]
    exr_path = os.path.join(model_output_folder, model_name+"-depth-1m-float32.exr")
    png_path = os.path.join(model_output_folder, model_name+"-depth-"+resolution+".png")

    print("Generating "+png_path)

    dmap = e2p.exr2arr(exr_path)[:,:,0]
    # zero background
    if dmap.dtype=='float32':
        dmap[dmap==10000000000.0]=0

    dmap = dmap/DMP
    dmap[dmap>65535]=0

    im = Image.fromarray(dmap.astype(np.uint16))
    im.save(png_path)

    #plt.imshow(dmap)
    #plt.colorbar()
    #plt.show()