import numpy as np
import cv2

# cap = cv2.VideoCapture('IMG_2744.m4v')
cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorMOG2()

while(True):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    fpm = cv2.bitwise_and(frame,frame,mask=fgmask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',fgmask)
    cv2.imshow('frameplusmask',fpm)

    ch = 0xFF & cv2.waitKey(1)
    if ch == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()