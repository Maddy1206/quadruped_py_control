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
import time
import math

sys.path.append('../lib/python/') # add a path variable that the library can be found by the python interpreter

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

    fS = 0.1
    rS = 0.13

    while True:
        time.sleep(0.01)
        motiontime = motiontime + 1

        udp.Recv()
        udp.GetRecv(state)

        if(motiontime > 0 and motiontime < 500):
            cmd.mode = 2
            cmd.forwardSpeed = fS

        if(motiontime > 500  and motiontime < 1000):
            cmd.mode = 2
            cmd.forwardSpeed = 0
            cmd.rotateSpeed = rS

        if(motiontime > 1000 and motiontime < 1500):
            cmd.mode = 2
            cmd.forwardSpeed = fS
            cmd.rotateSpeed = 0
        
        if(motiontime > 1500  and motiontime < 2000):
            cmd.mode = 2
            cmd.forwardSpeed = 0
            cmd.rotateSpeed = rS

        if(motiontime > 2000 and motiontime < 2500):
            cmd.mode = 2
            cmd.forwardSpeed = fS
            cmd.rotateSpeed = 0

        if(motiontime > 2500  and motiontime < 3000):
            cmd.mode = 2
            cmd.forwardSpeed = 0
            cmd.rotateSpeed = rS

        if(motiontime > 3000  and motiontime < 3500):
            cmd.mode = 2
            cmd.forwardSpeed = fS
            cmd.rotateSpeed = 0

        if(motiontime > 3500  and motiontime < 4000):
            cmd.mode = 2
            cmd.forwardSpeed = 0
            cmd.rotateSpeed = rS
        
        if(motiontime > 4000):
            cmd.mode = 1
            cmd.forwardSpeed = 0
            cmd.rotateSpeed = 0

        udp.SetSend(cmd)
        udp.Send()





