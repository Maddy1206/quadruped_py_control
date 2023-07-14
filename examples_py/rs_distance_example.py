##########################################################
#        Pythonic Robot Control for Unitree A1           #
#            for unitree_legged_sdk v3.2                 #
#    KISS Project at Hochschule Furtwangen University    #
##########################################################
# If you encounter any problems or need help in general, #
#         feel free to open an issue on GitHub           #
# ~ M. Untenberger                                       #
##########################################################

import sys 
sys.path.append('../lib/python')
import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()

config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
profile = pipeline.start(config)

try:
  while True:
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    distance = depth_frame.get_distance(320, 240)
    print(round(distance, 2))

    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    depth_colormap_dim = depth_colormap.shape
    color_colormap_dim = color_image.shape

    # If depth and color resolutions are different, resize color image to match depth image for display
    if depth_colormap_dim != color_colormap_dim:
        resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
        images = np.hstack((resized_color_image, depth_colormap))
    else:
        images = np.hstack((color_image, depth_colormap))

    cv2.rectangle(images,(320,240),(310,230),(0,0,255),-1)

    # Show images
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', images)
    cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()
    