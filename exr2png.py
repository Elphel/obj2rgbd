import OpenEXR
import Imath
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image

# From here: https://gist.github.com/arseniy-panfilov/4dc8fc5131277affe64619b1a9d00da0
def exr2arr(exrfile):
    file = OpenEXR.InputFile(exrfile)
    dw = file.header()['dataWindow']

    channels = file.header()['channels'].keys()
    print(channels)
    channels_list = list()
    for c in ('R', 'G', 'B', 'A'):
        if c in channels:
            channels_list.append(c)

    # the shape had incorrect order
    #size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    size = (dw.max.y - dw.min.y + 1, dw.max.x - dw.min.x + 1)
    color_channels = file.channels(channels_list, Imath.PixelType(Imath.PixelType.FLOAT))
    channels_tuple = [np.fromstring(channel, dtype='f') for channel in color_channels]
    res = np.dstack(channels_tuple)
    res.reshape(size + (len(channels_tuple),))
    return res[:,:,0]


if __name__ == "__main__":

    fname = "depth-0001.exr"
    arr = exr_to_array(fname)
    print(arr.shape)

    dmap = arr[:,:,0]
    print(np.max(dmap))

    dmap[dmap==65504]=0
    dmap[dmap==10000000000.0]=0

    print(np.max(dmap))

    k = 1
    #k = 0xffff/np.max(dmap)
    #k = 5 # 20cm
    k = 100 # 1 cm
    #k = 10 # 10cm /unit

    print("scale = "+str(k))
    dmap = k*dmap
    dmap[dmap>65535]=0

    im = Image.fromarray(dmap.astype(np.uint16))
    im.save('model-depth.png')

    plt.imshow(dmap)
    plt.colorbar()
    plt.show()