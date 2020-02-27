import os
import subprocess

import exr2png as e2p

PATH_TO_BLENDER = ""

fpaths = ['input/1527256815_550165_v01/1527256815_550165.obj',
            'input/1527256903_350165/v03/1527256903_350165.obj',
            'input/1488240695_710844_x3d105/1488240695_710844.obj']

filelist = ','.join(fpaths)

# this will run by Blender's bundled python
subprocess.run(os.path.join(PATH_TO_BLENDER,'blender')+" -b -P blender_generate_image_and_depth.py -- "+filelist, shell=True)

model_output_folder = "output"