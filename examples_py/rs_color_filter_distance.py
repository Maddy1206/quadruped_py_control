##########################################################
#        Pythonic Robot Control for Unitree A1           #
#            for unitree_legged_sdk v3.2                 #
#    KISS Project at Hochschule Furtwangen University    #
##########################################################
# If you encounter any problems or need help in general, #
#         feel free to open an issue on GitHub           #
# ~ M. Untenberger                                       #
##########################################################

"""
This Programm is making use of the hsv_color_filter.py and the rs_distance_example.py

First, you can change the colorfilter with the trackbars. You have to remove the remove the lower_green_bound and upper_green_bound
and make it dynamic. Otherwise the colorfilter is set to a specific type of green color.

Next, the program is returning a rectangle if it has found corresponding contour. The center of the rectangle is calculated and given to the pyrealsense2 library.
The distance is the returned from the center of the rectangle that has been found through the colorfilter.

You can also remove the align-depth2color functionality, as this is only mapping the depth to a specific color range. Nice to show but takes lots of computing power for little use.

There is also a rudimentary movement logic, which has to be tested extensively. this was only experimental.
"""

import sys, time, math
import numpy as np
import cv2

sys.path.append('/home/unitree/quadruped_py_control/lib/python') # change the path to the respective folder
import pyrealsense2 as rs           # Import the CPython Realsense library
import robot_interface as sdk       # Import the CPython Interface library

# Setting up robot utilities
HIGHLEVEL = 0x00
A1 = sdk.LeggedType.A1
BASIC = sdk.HighLevelType.Basic
SPORT = sdk.HighLevelType.Sport
udp = sdk.UDP(HIGHLEVEL, BASIC)
cmd = sdk.HighCmd()
state = sdk.HighState()
udp.InitCmdData(cmd)
motiontime = 0
cmd.forwardSpeed = 0
cmd.mode = 0
cmd.rotateSpeed = 0

# creat trackbars for color selection
def nothing(x):
    pass

cv2.namedWindow('TrackBars: Hue/Sat/Val')
cv2.moveWindow('TrackBars: Hue/Sat/Val',1320,0)
cv2.createTrackbar('HueMin', 'TrackBars: Hue/Sat/Val',  90,     179,nothing)
cv2.createTrackbar('HueMax', 'TrackBars: Hue/Sat/Val',  179,    179,nothing)
cv2.createTrackbar('SatMin', 'TrackBars: Hue/Sat/Val',  100,    255,nothing)
cv2.createTrackbar('SatMax', 'TrackBars: Hue/Sat/Val',  255,    255,nothing)
cv2.createTrackbar('ValMin', 'TrackBars: Hue/Sat/Val',  0,      255,nothing)
cv2.createTrackbar('ValMax', 'TrackBars: Hue/Sat/Val',  80,     255,nothing)

# create pipeline and configuration of depth and color streams
pipeline = rs.pipeline()
WIDTH = 640
HEIGHT = 480
config = rs.config()
config.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, WIDTH, HEIGHT, rs.format.z16, 30)

# start streaming
profile = pipeline.start(config)

# create align object -> allows to align depth frame to color frame
align_to = rs.stream.color
align = rs.align(align_to)

while True:
    # get frameset of color and depth
    frames = pipeline.wait_for_frames()

    # align depth frame to color frame
    aligned_frames = align.process(frames)

    # get aligned frames
    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    # convert to numpy arrays
    depth_image = np.asanyarray(aligned_depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # create trackbars for color selection
    hue_min = cv2.getTrackbarPos('HueMin', 'TrackBars: Hue/Sat/Val')
    hue_max = cv2.getTrackbarPos('HueMax', 'TrackBars: Hue/Sat/Val')
    sat_min = cv2.getTrackbarPos('SatMin', 'TrackBars: Hue/Sat/Val')
    sat_max = cv2.getTrackbarPos('SatMax', 'TrackBars: Hue/Sat/Val')
    val_min = cv2.getTrackbarPos('ValMin', 'TrackBars: Hue/Sat/Val')
    val_max = cv2.getTrackbarPos('ValMax', 'TrackBars: Hue/Sat/Val')
    lower_bound = np.array([hue_min, sat_min, val_min])
    upper_bound = np.array([hue_max, sat_max, val_max])
    lower_green_bound = np.array([90, 100, 0 ])
    upper_green_bound = np.array([179, 250, 80])
    colour_mask = cv2.inRange(color_image, lower_bound, upper_bound) # change variables to lower_bound and upper_bound to have the trackbars working

    cv2.imshow('Colour Mask', colour_mask)
    cv2.moveWindow('Colour Mask', 0, 0)

    # creat contour from region of interest
    contours, ret = cv2.findContours(colour_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        (x,y,w,h) = cv2.boundingRect(cnt)
        if area>=200:
            cv2.rectangle(color_image , (x,y), (x+w,y+h), (0,255,255), 3)
            break
        else:
            print("no contour detected")
            break

    

    # calculate center of region of interest
    center_rect_x = int(x+w/2)
    center_rect_y = int(y+h/2)
    print(center_rect_x, center_rect_y)

    # get distance from center of region of interest
    distance = aligned_depth_frame.get_distance(center_rect_x, center_rect_y)
    print(round(distance, 2))

    # program movements of the robot
    diff = 50 # pixel safe space for robust movement
    if distance == 0:
        continue

    if center_rect_x > WIDTH/2+diff:
        cmd.mode = 2
        cmd.rotateSpeed = 0.3
        print("rotating right")

    if center_rect_x < WIDTH/2-diff:
        cmd.mode = 2
        cmd.rotateSpeed = -0.3
        print("rotating left")

    if center_rect_x > WIDTH/2-diff and center_rect_x < WIDTH/2+diff:
        cmd.mode = 2
        cmd.rotateSpeed = 0
        print("waiting in rotate loop")

    if distance < 1:
        cmd.mode = 2
        cmd.forwardSpeed = -0.3
        print("walking backwards\n")

    if distance > 1.3:
        cmd.mode = 2
        cmd.forwardSpeed = 0.3
        print("walking forward\n")

    if distance > 1 and distance < 1.3:
        cmd.mode = 0
        cmd.forwardSpeed = 0
        print("waiting in forward loop")
    

    # render images
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    images = np.hstack((color_image, depth_colormap))

    cv2.imshow('Align Example', images)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break

pipeline.stop()
cv2.destroyAllWindows()
