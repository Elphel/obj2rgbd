'''
Copyright (C) 2020, Elphel Inc.
SPDX-License-Identifier: GPL-3.0-or-later
Author: Oleg K Dzhimiev <oleg@elphel.com>
'''

'''
Usage:

~$ blender -b -P blender_generate_image_and_depth.py -- file1,file2,..,fileN
or
~$ <path-to-blender>/blender -b -P blender_generate_image_and_depth.py -- file1,file2,..,fileN

Notes:
  - *.obj format
  - include path in the *.obj name
  - unique *.obj names - everything is dumped into a single folder
  - .mtl and textures, if exist, must be in the *.obj path
  - no spaces after commas in the file list
  - blender executable must be in the path
    - ~$ which blender
    - alternatively can call from blender path

Example:

~$ blender -b -P blender_generate_image_and_depth.py -- path1/model1.obj,path2/model2.obj

Output:

  - <model_output_folder>/name-image.jpeg - RGB
  - <model_output_folder>/name-depth.exr  - D, 32-bit float data

Comment:

  - for some reason it worked ok with Blender v2.80.75
  - didn't work for some models in Blender v2.82.7

'''
import numpy as np
import os
import sys

import bpy

# hardcoded constants
img_w = 2592
img_h = 1902
img_fov_degs = 66.8

model_default_rotation = (90*np.pi/180.0, 0, 0)
model_output_folder = "output"
# end constants

scene = bpy.context.scene
world = scene.world
camera = scene.camera

# fixed resolution for now
scene.render.resolution_x = img_w
scene.render.resolution_y = img_h
scene.render.resolution_percentage = 100

world.use_nodes = False
world.color = (1.00 , 1.00 , 1.00)

objs = bpy.data.objects
objs.remove(objs["Cube"], do_unlink=True)
objs.remove(objs["Light"], do_unlink=True)

camera.location = (0,0,0)
camera.rotation_mode = "XYZ"
camera.rotation_euler = model_default_rotation
camera.data.clip_end = 10000
camera.data.clip_start = 0.1
camera.data.angle = img_fov_degs*np.pi/180

bpy.context.scene.use_nodes = True

rn = scene.node_tree.nodes.new('CompositorNodeRLayers')
depth = scene.node_tree.nodes.new('CompositorNodeOutputFile')
depth.format.file_format = 'OPEN_EXR'
depth.format.color_depth = '32'
# TODO: try BW
depth.format.color_mode = 'RGB'
depth.format.exr_codec = 'ZIP'
depth.base_path = model_output_folder
depth.file_slots[0].path = 'depth-'

scene.node_tree.links.new(rn.outputs[2], depth.inputs[0])

fpaths = sys.argv[-1].split(',')

if(not (os.path.isdir(model_output_folder))):
    os.mkdir(model_output_folder)

for fpath in fpaths:

    obj_name = fpath.split('/')[-1][:-4]

    bpy.ops.import_scene.obj(filepath=fpath, use_smooth_groups=False)

    obj = bpy.data.objects[obj_name]
    for mat in obj.material_slots:
        mat.material.use_nodes = True

    scene.render.filepath = os.path.join(model_output_folder,obj_name+"-image.jpeg")
    scene.render.image_settings.file_format='JPEG'
    bpy.ops.render.render(write_still = True)
    bpy.data.objects.remove(obj)
    # rename exr
    os.rename(os.path.join(model_output_folder,'depth-0001.exr'),os.path.join(model_output_folder,obj_name+"-depth.exr"))


