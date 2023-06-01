#!/usr/bin/python

#############################################################
#           Pythonic Robot Control for Unitree A1           #
#               for unitree_legged_sdk v3.2                 #
#       KISS Project at Hochschule Furtwangen University    #
#############################################################

import sys
import time
import math

sys.path.append('/home/ros/unitree_legged_sdk_py11/lib/python')

import robot_interface as sdk       # Import the CPython library 

if __name__ == '__main__':

    HIGHLEVEL = 0x00
    LOWLEVEL = 0xff

    A1 = sdk.LeggedType.A1

    BASIC = sdk.HighLevelType.Basic
    SPORT = sdk.HighLevelType.Sport

    udp = sdk.UDP(HIGHLEVEL, BASIC)

    cmd = sdk.HighCmd()
    state = sdk.HighState()
    udp.InitCmdData(cmd)
    motiontime = 0

    cmd.forwardSpeed = 0
    cmd.sideSpeed = 0
    cmd.rotateSpeed = 0
    cmd.bodyHeight = 0

    cmd.mode = 0
    cmd.roll = 0
    cmd.pitch = 0
    cmd.yaw = 0

    while True:
        time.sleep(0.01)
        motiontime = motiontime + 1

        udp.Recv()
        udp.GetRecv(state)

        print(motiontime)
        # print(state.imu.temperature)

        if(motiontime > 0 and motiontime < 1000):
            cmd.mode = 2
            cmd.forwardSpeed = 0.3
            print("walk\n")

        udp.SetSend(cmd)
        udp.Send()

        if(motiontime > 1000):
            break



