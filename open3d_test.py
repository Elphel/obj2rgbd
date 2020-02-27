# From here: http://www.open3d.org/docs/release/tutorial/Basic/rgbd_images/redwood.html
# examples/Python/Basic/rgbd_redwood.py

import open3d as o3d
import matplotlib.pyplot as plt
import sys

if __name__ == "__main__":

    image_path = "output/example-test_cube-image.jpeg"
    depth_path = "output/example-test_cube-depth-10cm.png"

    try:
        image_path = sys.argv[1]
        depth_path = sys.argv[2]
    except IndexError:
        pass

    color_raw = o3d.io.read_image(image_path)
    depth_raw = o3d.io.read_image(depth_path)
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color_raw, depth_raw)
    print(rgbd_image)

    plt.subplot(1, 2, 1)
    plt.title('Grayscale image')
    plt.imshow(rgbd_image.color)
    plt.subplot(1, 2, 2)
    plt.title('Depth image')
    plt.imshow(rgbd_image.depth)
    plt.show()

    psd = o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault
    #pci0 = o3d.camera.PinholeCameraIntrinsic(psd)
    #pci0 = o3d.camera.PinholeCameraIntrinsic(2592, 1902, 2045, 2045, 1296, 951)
    #fx = fy = 2045
    # based on 66.8 hfov and 2592 pixels
    fx = fy = 1965
    pci0 = o3d.camera.PinholeCameraIntrinsic(2592, 1902, fx, fy, 1296, 951)

    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
        rgbd_image,
        pci0)
    # Flip it, otherwise the pointcloud will be upside down
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    o3d.visualization.draw_geometries([pcd])
