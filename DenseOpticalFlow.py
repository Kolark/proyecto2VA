import numpy as np
import cv2
import smoothPrediction

prediction = smoothPrediction.Prediction(5)


class DenseOpticalFlow:
    def __init__(self,starterFrame):
        self.current = starterFrame
        self.current = cv2.GaussianBlur(self.current,(5,5),0)
        self.previous =  cv2.cvtColor(self.current,cv2.COLOR_BGR2GRAY)
        print("")

    def UpdateFrame(self,frame):
        # self.previous = self.current
        self.current = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        self.current = cv2.GaussianBlur(self.current,(5,5),0)
        self.flow = cv2.calcOpticalFlowFarneback(self.previous,self.current, None, 0.5, 3,15, 3, 5, 1.2, 0)
        
        h,w,c = frame.shape
        zeros = np.zeros((h,w),np.uint8)


        flowX = self.flow[:,:,0]
        flowY = self.flow[:,:,1]

        flowX = flowX**2
        flowY = flowY**2

        self.flowMagnitud = np.sqrt(flowX + flowY)
    
        self.flowmean = np.mean(self.flowMagnitud)

        self.mValue = prediction.Update(self.flowmean)
        print(self.mValue)
        self.previous=self.current



    print("Update Frame")

    