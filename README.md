# Description
Batch generate RGB-D format image pairs from *.obj models with textures in command line using Blender python script.

# Quickstart
```
~$ python3 obj2rgbd.py
~$ python3 open3d_test.py
```

# Requirements
* Blender 2.80 (need to test 2.82 - didn't work for some models)
* Python3: **numpy, matplotlib, Pillow, OpenEXR, open3d (optional)**
* Tested in Kubuntu 16.04

# Setup

## Blender

* Get Blender 2.80 (need to test 2.82 - didn't work for some models)
* Add Blender's path to your ~/.bashrc:
```
export PATH="/home/$USER/Downloads/blender-2.80-linux-glibc217-x86_64:$PATH"
```

## Python 3

* numpy, matplotlib, pillow and open3d are trivially installed
* OpenEXR
```
pip install openexr
```
When it failed to install this [link](https://stackoverflow.com/questions/45601949/install-openexr-in-python-doesnt-work) helped.

# Details

## obj2rgbd.py

```~$ python3 obj2rgbd.py [input_folder [depth_map_resolution]]```:

*input_folder* - folder with subfolders with *.obj files, default value - **input**

*depth_map_resolution* - units in the depth 16-bit *.png file, default value - **0.1**, which is 10cm allowing for **0-6553.5 m** range

| Value | Depth resolution | Depth range |
| ------ | :------: | ------ |
|1|1 m|0-65535 m|
|0.1|10 cm|0-6553.5 m|
|0.01|1 cm|0-655.35 m|
|0.001|1 mm|0-65.535 m|

What it does:
1. Makes a list of all *.obj models found in a given input folder's subfolders
2. Runs Blender feeding it with the *blender_generate_image_and_depth.py* and the list
3. Blender script saves results into **output/** (auto created). A single result is a rendered image of a model and the depth buffer saved into 32-bit float *.exr format
4. After Blender is done for all models *obj2rgbd.py* then generates 16-bit *.png depth images with a given resolution from *.exr files. Results are also in the **output/**

Example:
1. 10cm depth resolution
```
~$ python3 obj2rgbd.py input 0.1
```

## open3d_test.py

```~$ python3 open3d_test.py [path-to-image-file [path-to-depth-file]]```:

*path-to-image-file* - jpeg, defaults to **output/example-test_cube-image.jpeg**

*path-to-depth-file* - 16-bit png, defaults to **output/example-test_cube-depth-10cm.png**

What is does:
1. Opens RGB-D pair using Open3D python library. First it displays side-to-side, upon closing the first plot - it display a 3D view.
2. Hardcoded parameters inside the script: w=2592, h=1902, fx=fy=2045, cx=1296, cy=951

Example:
```
~$ python3 open3d_test.py output/example-test_cube-image.jpeg output/example-test_cube-depth-10cm.png
```

## blender_generate_image_and_depth.py

Can be run standalone:
```
~$ blender -b -P blender_generate_image_and_depth.py -- path1/model1.obj,path2/model2.obj
```

# Notes

* Can have multiple models in the same subfolder
* Model names need to be unique as the output files are dumped in a single **output/** folder
* *.obj filename must match with the name inside it. See example model in **input/**
* *obj2rgbd.py* running ```blender -b -P blender_generate_image_and_depth.py -- filelist``` - Blender runs *blender_generate_image_and_depth.py* using its bundled python (Python 3.7 in Blender 2.80). Could have a single script for everything but it's too much effort to install openexr to that bundled python.

# More models

https://community.elphel.com/3d+map

https://community.elphel.com/3d+biquad

Loading everything can take some time. Once loaded there's a download button in the top-right menu.