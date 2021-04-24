import numpy as np
import cv2 as cv
import smoothPrediction


prediction = smoothPrediction.Prediction(5)
cap = cv.VideoCapture(0)
ret, frame1 = cap.read()
frame1 = cv.GaussianBlur(frame1,(5,5),0)

prvs = cv.cvtColor(frame1,cv.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255
while(1):
    ret, frame2 = cap.read()
    frame2 = cv.GaussianBlur(frame2,(5,5),0)
    next = cv.cvtColor(frame2,cv.COLOR_BGR2GRAY)
    flow = cv.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3,15, 3, 5, 1.2, 0)
    
    h,w,c = frame2.shape
    zeros = np.zeros((h,w),np.uint8)


    flowX = flow[:,:,0]
    flowY = flow[:,:,1]

    flowX = flowX**2
    flowY = flowY**2

    flowMagnitud = np.sqrt(flowX+flowY)
    
    flowmean = np.mean(flowMagnitud)

    mValue = prediction.Update(flowmean)

    print("flowmean " + str(flowmean) + "     value " + str(mValue))

    mag, ang = cv.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv.normalize(mag,None,0,255,cv.NORM_MINMAX)
    bgr = cv.cvtColor(hsv,cv.COLOR_HSV2BGR)
    cv.imshow('frame2',bgr)
    k = cv.waitKey(1) & 0xff
    if k == 27:
        break
    prvs = next