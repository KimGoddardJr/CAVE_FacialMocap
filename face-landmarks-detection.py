
# [1] Qt5/OpenCV window code modified from:
# https://www.codepile.net/pile/ey9KAnxn

# [2] Face landmark detection code modified from:
# https://pysource.com/2019/03/12/face-landmarks-detection-opencv-with-python/
# [3] Head pose estimation code modified from:
# https://learnopencv.com/head-pose-estimation-using-opencv-and-dlib/
# (See P.I. submission for full references)

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import cv2
import numpy as np
import dlib

showFaceTrack = True
showLandmarks = True

class ShapePredictor:
    def __init__(self):
        # identify key landmarks for face direction
        self.numLandmarks = 68
        self.chin = 9
        self.nose = 34
        self.left_eye = 37
        self.right_eye = 46
        self.left_mouth = 49
        self.right_mouth = 55

        self.frame = None
        self.Grey_Image = None

        # shape_predictor_68_face_landmarks.dat file must be in same directory
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    def setImgFrame(self, frame):
        self.Grey_Image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  
    def getFaces(self):
        #Run Face Detection
        faces = self.detector(self.Grey_Image)
        return faces

    def getLandmarks(self, face):
        #Get Facial Landmarks
        landmarks = self.predictor(self.Grey_Image, face)
        return landmarks

    def poseEstimation(self):
        #2D capture points:
            cap_points = np.array([
                                    (self.landmarks.part(self.nose-1).x, self.landmarks.part(self.nose-1).y),     
                                    (self.landmarks.part(self.chin-1).x, self.landmarks.part(self.chin-1).y),     # Chin
                                    (self.landmarks.part(self.left_eye-1).x, self.landmarks.part(self.left_eye-1).y),     # Left eye left corner
                                    (self.landmarks.part(self.right_eye-1).x, self.landmarks.part(self.right_eye-1).y),     # Right eye right corne
                                    (self.landmarks.part(self.left_mouth-1).x, self.landmarks.part(self.left_mouth-1).y),     # Left Mouth corner
                                    (self.landmarks.part(self.right_mouth-1).x, self.landmarks.part(self.right_mouth-1).y)      # Right mouth corner
                                ], dtype="double")

            # 3D model points (taken from [3])
            model_points = np.array([
                                    (0.0, 0.0, 0.0),             # Nose tip
                                    (0.0, -330.0, -65.0),        # Chin
                                    (-225.0, 170.0, -135.0),     # Left eye left corner
                                    (225.0, 170.0, -135.0),      # Right eye right corne
                                    (-150.0, -150.0, -125.0),    # Left Mouth corner
                                    (150.0, -150.0, -125.0)      # Right mouth corner
                                ])

            # Camera internals
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT )

            focal_length = width
            center = (width/2, height/2)
            camera_matrix = np.array(
                                    [[focal_length, 0, center[0]],
                                    [0, focal_length, center[1]],
                                    [0, 0, 1]], dtype = "double"
                                    )

            dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
            (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, cap_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

            (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

            for p in cap_points:
                cv2.circle(frame, (int(p[0]), int(p[1])), 3, (0,0,255), -1)

            p1 = ( int(cap_points[0][0]), int(cap_points[0][1]))
            p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

            cv2.line(frame, p1, p2, (255,0,0), 2)
        #outside for loop: cv2.imshow("Frame",frame)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        title = "OpenCV Face Mocap [WIP] - s5400010"
        self.setWindowTitle(title)

        self.VBL = QVBoxLayout()

        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        #Buttons
        self.CancelBtn = QPushButton("Cancel")
        self.CancelBtn.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBtn)

        self.ToggleFaceLoc = QPushButton("Show/Hide Face Track")
        self.ToggleFaceLoc.clicked.connect(self.TglFaceLoc)
        self.VBL.addWidget(self.ToggleFaceLoc)

        self.ToggleLandmarks = QPushButton("Show/Hide Landmarks")
        self.ToggleLandmarks.clicked.connect(self.TglLandmarks)
        self.VBL.addWidget(self.ToggleLandmarks)

        self.CameraThread = Camera_Worker()

        self.CameraThread.start()
        self.CameraThread.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)


    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.CameraThread.stop()

    def TglFaceLoc(self):
        global showFaceTrack
        showFaceTrack = not showFaceTrack

    def TglLandmarks(self):
        global showLandmarks 
        showLandmarks = not showLandmarks

class Camera_Worker(QThread):

    ImageUpdate = pyqtSignal(QImage)
    Face = ShapePredictor()
    cap = cv2.VideoCapture(0)

    def run(self):
        self.ThreadActive = True
        print("Attempt capture...")

        while self.ThreadActive:
            _, frame = self.cap.read()


            if _:
                #Get OpenCV Image
                self.Face.setImgFrame(frame)
                faces = self.Face.getFaces()

                for face in faces:
                    if showFaceTrack:
                        self.displayFaceTrack(face, frame)

                    if showLandmarks:
                        landmarks = self.Face.getLandmarks(face)
                        self.displayLandmarks(landmarks, frame)


                RGB_Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #Grey_Image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                FlippedImage = cv2.flip(RGB_Image, 1)

                #Convert to Qt Image
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                #ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_Grayscale8)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
            else: print("ret = false")
    def stop(self):
        print("Stop feed...")
        self.ThreadActive = False
        self.quit()

    def displayNose(self, frame, landmarks):
        x = landmarks.part(self.nose-1).x
        y = landmarks.part(self.nose-1).y
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

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())