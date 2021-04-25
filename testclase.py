import numpy as np
import cv2 as cv
import smoothPrediction
import DenseOpticalFlow

prediction = smoothPrediction.Prediction(5)
cap = cv.VideoCapture(0)
ret, frame1 = cap.read()
DOpticalFlow = DenseOpticalFlow.DenseOpticalFlow(frame1) 

hsv = np.zeros_like(frame1)
hsv[...,1] = 255
while(1):
    ret, frame2 = cap.read()
    DOpticalFlow.UpdateFrame(frame2)

    mag, ang = cv.cartToPolar(DOpticalFlow.flow[...,0], DOpticalFlow.flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv.normalize(mag,None,0,255,cv.NORM_MINMAX)
    bgr = cv.cvtColor(hsv,cv.COLOR_HSV2BGR)
    cv.imshow('frame2',bgr)
    k = cv.waitKey(1) & 0xff
    if k == 27:
        break