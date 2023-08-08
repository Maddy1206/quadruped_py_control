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

sys.path.append('../lib/python/') # add a path variable that the library can be found by the python interpreter

import robot_interface as sdk       # Import the CPython library 

if __name__ == '__main__':

    HIGHLEVEL = 0x00
    LOWLEVEL = 0xff

    A1 = sdk.LeggedType.A1

    BASIC = sdk.HighLevelType.Basic
    SPORT = sdk.HighLevelType.Sport

    udp = sdk.UDP(LOWLEVEL, BASIC)

    cmd = sdk.LowCmd()
    state = sdk.LowState()
    udp.InitCmdData(cmd)
    safe = sdk.Safety(A1)

    joint_dict = {
        "FR_0": 0, "FR_0": 1, "FR_2": 2, # Front Right; 0 = Shoulder (inwards), 1 = Shoulder (outwards), 2 = leg joint
        
        "FL_0": 3, "FL_0": 4, "FL_2": 5, # Front Left; 0 = Shoulder (inwards), 1 = Shoulder (outwards), 2 = leg joint

        "RR_0": 6, "RR_1": 7, "RR_2": 8, # Rear Right; 0 = Shoulder (inwards), 1 = Shoulder (outwards), 2 = leg joint

        "RL_0": 9, "RL_1": 10, "RL2": 11, # Rear Left; 0 = Shoulder (inwards), 1 = Shoulder (outwards), 2 = leg joint
    }
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
        print("states on front right shoulder (inwards):")
        print(state.motorState[0].q)
        print(state.motorState[0].dq)
        print(state.motorState[0].dq)

        
        
        ### examples as to initialize movements can be found in the example_velocity.cpp, example_position.cpp and example_torque.cpp.
        
        udp.SetSend(cmd)
        udp.Send()





