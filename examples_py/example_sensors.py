##########################################################
#        Pythonic Robot Control for Unitree A1           #
#            for unitree_legged_sdk v3.2                 #
#    KISS Project at Hochschule Furtwangen University    #
##########################################################
# If you encounter any problems or need help in general, #
#         feel free to open an issue on GitHub           #
##########################################################

import sys
import time

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

    while True:
        time.sleep(0.01)

        udp.Recv()
        udp.GetRecv(state)

        print(state.imu.rpy[0])
        print("Forces on feet: ")
        print(state.footForce[0], state.footForce[1], state.footForce[2], state.footForce[3])
        print("Foot position relative to body: ")
        print(state.footPosition2Body[0].x)
        print(state.footPosition2Body[0].y)
        print(state.footPosition2Body[0].z, "\n")

        # print(state.imu.temperature)
        
        ### for more readable sensors, have a look in the comm.h file inside the include-folder
        ### there you can find which sensors can be initialized
        
        udp.SetSend(cmd)
        udp.Send()





