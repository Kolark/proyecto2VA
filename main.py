#Import libraries
import sys,re
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

import cv2
import numpy as np


#.ui file path
uiFile = "./ui/mainFrame.ui"
#Load ui file
Ui_MainWindow, QtBaseClass = uic.loadUiType(uiFile)
#Capture video
captura = cv2.VideoCapture(0)


class UIWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.controlTimer()
    
    def viewCam(self):
    # read imageS in BGR format
        disponible, fotograma = captura.read()
        fotograma = cv2.flip(fotograma,1)
        h, w, channel = fotograma.shape    

    # convert image to RGB format
        fotogramaRGB = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
        self.SetImages(fotogramaRGB,self.imgWidget)

    def SetImages(self,IMG,label):
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
    app =  QtWidgets.QApplication(sys.argv)
    window = UIWindow()
    window.show()
    sys.exit(app.exec_())