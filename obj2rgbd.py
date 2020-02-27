import os
import subprocess

PATH_TO_BLENDER = ''
# depth map scale, units in the generated depth map for RGB-D - 16-bit png
#DMP = 1   # 1 m - range 0-65535 m
#DMP = 0.1 # 10 cm - range 0-6553.5 m
DMP = 0.01 # 1 cm  - range 0-655.35 m
#DMP = 0.001 # 1 mm  - range 0-65.535 m

fpaths = ['input/1527256815_550165_v01/1527256815_550165.obj',]

filelist = ','.join(fpaths)

# this will run by Blender's bundled python
subprocess.run(os.path.join(PATH_TO_BLENDER,'blender')+" -b -P blender_generate_image_and_depth.py -- "+filelist, shell=True)

fname = '1527256815_550165-depth.exr'

model_output_folder = "output"

fname = os.path.join(model_output_folder,fname)

import exr2png as e2p
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

dmap = e2p.exr2arr(fname)[:,:,0]
# zero background
if dmap.dtype=='float32':
    dmap[dmap==10000000000.0]=0

dmap = dmap/DMP
dmap[dmap>65535]=0

im = Image.fromarray(dmap.astype(np.uint16))
im.save(os.path.join(model_output_folder,'model-depth.png'))

plt.imshow(dmap)
plt.colorbar()
plt.show()