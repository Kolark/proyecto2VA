# Import libraries
import sys
import re
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
# OTHER IMPORTS
import cv2
import numpy as np
import smoothPrediction
import DenseOpticalFlow

from pose_prediction.pose_estimation_angles import PoseEstimation

import keyboard

# ---------------------
prediction = smoothPrediction.Prediction(5)
# .ui file path
uiFile = "./ui/mainFrame.ui"
# Load ui file
Ui_MainWindow, QtBaseClass = uic.loadUiType(uiFile)
# Capture video
captura = cv2.VideoCapture(0)
# -----------------------------------
ret, frame1 = captura.read()
DOpticalFlow = DenseOpticalFlow.DenseOpticalFlow(frame1)
hsv = np.zeros_like(frame1)
hsv[..., 1] = 255
movementThreshold = 0.6


class UIWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pixmap = QPixmap('imgreference.PNG')
        
        self.imgref.setPixmap(self.pixmap)
        
        self.pose_estimation = PoseEstimation()

        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.controlTimer()
        self.is_pose = False

    def viewCam(self):
        # read imageS in BGR format
        disponible, fotograma = captura.read()
        fotograma = cv2.flip(fotograma, 1)

        DOpticalFlow.UpdateFrame(fotograma)

        h, w, channel = fotograma.shape

        mag, ang = cv2.cartToPolar(
            DOpticalFlow.flow[..., 0], DOpticalFlow.flow[..., 1])
        hsv[..., 0] = ang*180/np.pi/2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # convert image to RGB format
        fotogramaRGB = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
        self.SetImages(fotogramaRGB, self.imgWidget)
        self.SetImages(bgr, self.img_)
        print(DOpticalFlow.mValue)
        if DOpticalFlow.mValue > 0.45:
            keyboard.press('right')
            keyboard.release('left')
        else:
            self.is_pose = self.pose_estimation.is_in_pose(fotogramaRGB)

            if self.is_pose:
                keyboard.press('left')
                keyboard.release('right')
            else:
                keyboard.release('left')
                keyboard.release('right')

        # self.magnitud.setText(str(DOpticalFlow.mValue))
        self.magnitud.setText("Is in pose" if self.is_pose else "Not in pose")

    def SetImages(self, IMG, label):
        h, w, channel = IMG.shape
        step = channel * w
        qImg = QImage(IMG.data, w, h, step, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qImg))

    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(16)
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UIWindow()
    window.show()
    sys.exit(app.exec_())
