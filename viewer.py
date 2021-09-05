# [1] Qt5/OpenCV window code modified from:
# https://www.codepile.net/pile/ey9KAnxn

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from face_prediction import ShapePredictor

import cv2
import numpy as np

streamEnabled = True
showFaceTrack = False
showLandmarks = False
showNose = False
showPose = True

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        #Window
        title = "OpenCV Face Mocap [WIP] - s5400010"
        self.setWindowTitle(title)

        #uic.loadUi('MainWindow.ui', self)

        self.VBL = QVBoxLayout()

        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        #Buttons
        self.CancelBtn = QPushButton("Start/Stop Camera Feed")
        self.CancelBtn.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBtn)

        self.ToggleFaceLoc = QPushButton("Show/Hide Face Track")
        self.ToggleFaceLoc.clicked.connect(self.TglFaceLoc)
        self.VBL.addWidget(self.ToggleFaceLoc)

        self.ToggleLandmarks = QPushButton("Show/Hide Landmarks")
        self.ToggleLandmarks.clicked.connect(self.TglLandmarks)
        self.VBL.addWidget(self.ToggleLandmarks)

        self.Toggle3DPose = QPushButton("Show Pose Estimation")
        self.Toggle3DPose.clicked.connect(self.TglPose)
        self.VBL.addWidget(self.Toggle3DPose)

        self.enableFile = QCheckBox("Write to File")
        self.enableFile.setChecked(True)
        self.enableFile.setEnabled(False)
        self.VBL.addWidget(self.enableFile)

        #Workers
        self.CameraThread = Camera_Worker()
        if streamEnabled == True:
            self.CameraThread.start()
        self.CameraThread.ImageUpdate.connect(self.ImageUpdateSlot)

        # Child layout to Window
        self.setLayout(self.VBL)
        
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        global streamEnabled
        streamEnabled = not streamEnabled

        if streamEnabled == True:
            self.CameraThread.start()

        else:
            self.CameraThread.stop()

    def TglFaceLoc(self):
        global showFaceTrack
        showFaceTrack = not showFaceTrack

    def TglLandmarks(self):
        global showLandmarks 
        showLandmarks = not showLandmarks

    def TglPose(self):
        global showPose
        showPose = not showPose



class Camera_Worker(QThread):

    ImageUpdate = pyqtSignal(QImage)

    Face = ShapePredictor()

    cap = cv2.VideoCapture(0)
    frame = None
    width = 0
    height = 0

    def run(self):
        self.ThreadActive = True
        print("Attempt capture...")

        self.getCameraMatrix()

        while self.ThreadActive:
            _, self.frame = self.cap.read()

            if _:
                #Get OpenCV Image
                self.Face.setImgFrame(self.frame)
                faces = self.Face.getFaces()

                for face in faces:
                    if showFaceTrack:
                        self.displayFaceTrack(face, self.frame)

                    if showLandmarks:
                        landmarks = self.Face.getLandmarks(face)
                        self.displayLandmarks(landmarks, self.frame)

                    if showPose:
                        landmarks = self.Face.getLandmarks(face)
                        end_point2D = self.poseEstimation(self.frame)

                        p1 = ( landmarks.part(34-1).x, landmarks.part(34-1).y) #todo: get nose
                        p2 = ( int(end_point2D[0][0][0]), int(end_point2D[0][0][1]))

                        cv2.line(self.frame, p1, p2, (0,0,255), 2)
                        
                    if showNose:
                        landmarks = self.Face.getLandmarks(face)
                        self.displayNose(self.frame, landmarks)

                RGB_Image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(RGB_Image, 1)

                #Convert to Qt Image
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
            
    def stop(self):
        print("Stop feed...")
        self.ThreadActive = False
        self.quit()

    def getCameraMatrix(self):
        # Camera internals
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH )
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT )
        
        focal_length = self.width
        center = (self.width/2, self.height/2)
        camera_matrix = np.array(
                                [[focal_length, 0, center[0]],
                                [0, focal_length, center[1]],
                                [0, 0, 1]], dtype = "double"
                                )
                            
        return camera_matrix
        

    def displayNose(self, frame, landmarks):
        x = landmarks.part(34-1).x #todo: get nose
        y = landmarks.part(34-1).y
        cv2.circle(frame, (x, y), 4, (255, 255, 255), -1)

    def displayFaceTrack(self, face, frame):
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

    def displayLandmarks(self, landmarks, frame):
        for n in range(0, 68): #todo: update numLandmarks
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)

    def poseEstimation(self, frame):

        camera_matrix = self.getCameraMatrix()
        dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion

        return self.Face.getCapPoints(camera_matrix, dist_coeffs)
