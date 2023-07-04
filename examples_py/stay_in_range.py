##########################################################
#        Pythonic Robot Control for Unitree A1           #
#            for unitree_legged_sdk v3.2                 #
#    KISS Project at Hochschule Furtwangen University    #
##########################################################
# If you encounter any problems or need help in general, #
#         feel free to open an issue on GitHub           #
# ~ M. Untenberger                                       #
##########################################################

import sys, time, math
import numpy as np
import cv2

sys.path.append('/home/unitree/quadruped_py_control/lib/python') # change the path to the respective folder
import pyrealsense2 as rs           # Import the CPython Realsense library
import robot_interface as sdk       # Import the CPython Interface library


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
cmd.sideSpeed = 0.15 # nullify uneven calibration

pipeline = rs.pipeline()
config = rs.config()
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)


profile = pipeline.start(config)

while True:
  frames = pipeline.wait_for_frames()
  depth_frame = frames.get_depth_frame()
  # color_frame = frames.get_color_frame()

  distance = depth_frame.get_distance(320, 240)
  print(round(distance, 2))

  udp.Recv()
  udp.GetRecv(state)

  if distance == 0:
      continue

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
    print("waiting...")

  udp.SetSend(cmd)
  udp.Send()
