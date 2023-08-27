##########################################################
#        Pythonic Robot Control for Unitree A1           #
#            for unitree_legged_sdk v3.2                 #
#    KISS Project at Hochschule Furtwangen University    #
##########################################################
# If you encounter any problems or need help in general, #
#         feel free to open an issue on GitHub           #
##########################################################

import cv2
import numpy as np
import time

print(cv2.__version__)
timeMark=time.time()
dtFIL=0

def nothing(x):
    pass

cv2.namedWindow('TrackBars: Hue/Sat/Val')
cv2.moveWindow('TrackBars: Hue/Sat/Val',1320,0)
cv2.createTrackbar('HueMin', 'TrackBars: Hue/Sat/Val',100,179,nothing)
cv2.createTrackbar('HueMax', 'TrackBars: Hue/Sat/Val',116,179,nothing)
cv2.createTrackbar('SatMin', 'TrackBars: Hue/Sat/Val',160,255,nothing)
cv2.createTrackbar('SatMax', 'TrackBars: Hue/Sat/Val',255,255,nothing)
cv2.createTrackbar('ValMin', 'TrackBars: Hue/Sat/Val',150,255,nothing)
cv2.createTrackbar('ValMax', 'TrackBars: Hue/Sat/Val',255,255,nothing)


width = 720
height = 480
font = cv2.FONT_HERSHEY_SIMPLEX

cam=cv2.VideoCapture(0)

while True:
    ret, frame1 = cam.read()

    hsv = cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV)

    # https://learnopencv.com/color-spaces-in-opencv-cpp-python/?ref=blog.electroica.com
    hue_min = cv2.getTrackbarPos('HueMin', 'TrackBars: Hue/Sat/Val')
    hue_max = cv2.getTrackbarPos('HueMax', 'TrackBars: Hue/Sat/Val')
    sat_min = cv2.getTrackbarPos('SatMin', 'TrackBars: Hue/Sat/Val')
    sat_max = cv2.getTrackbarPos('SatMax', 'TrackBars: Hue/Sat/Val')
    val_min = cv2.getTrackbarPos('ValMin', 'TrackBars: Hue/Sat/Val')
    val_max = cv2.getTrackbarPos('ValMax', 'TrackBars: Hue/Sat/Val')
    lower_bound=np.array([hue_min, sat_min, val_min])
    upper_bound=np.array([hue_max, sat_max, val_max])

    colour_mask = cv2.inRange(hsv, lower_bound, upper_bound)

    cv2.imshow('Colour Mask', colour_mask)
    cv2.moveWindow('Colour Mask', 0, 0)

    contours1, ret = cv2.findContours(colour_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours1 = sorted(contours1, key=lambda x:cv2.contourArea(x), reverse=True)
    for cnt in contours1:
        area = cv2.contourArea(cnt)
        (x,y,w,h) = cv2.boundingRect(cnt)
        if area>=100:
            cv2.rectangle(frame1 , (x,y), (x+w,y+h), (0,255,255), 3)
            break

    frame3=frame1 # np.hstack((frame1))
    dt=time.time()-timeMark
    timeMark=time.time()
    dtFIL=.9*dtFIL + .1*dt
    fps=1/dtFIL
    cv2.rectangle(frame3,(0,0),(150,40),(0,0,255),-1)
    cv2.putText(frame3,'fps: '+str(round(fps,1)),(0,30),font,1,(255,255,255),2)

    cv2.imshow('OG Vid',frame3)
    cv2.moveWindow('OG Vid',0,450)

    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()