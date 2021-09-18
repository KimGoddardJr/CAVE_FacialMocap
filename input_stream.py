from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt3DCore import *
from PyQt5.Qt3DExtras import *

from face_prediction import *


class Camera_Worker(QThread):

    ImageUpdate = pyqtSignal(QImage)
    Face = SP_68points()

    cap = cv2.VideoCapture(0)

    frame = None
    width = 0
    height = 0

    #Display option flags
    showFaceTrack = False
    showLandmarks = False
    showNose = False
    showPose = False

    def run(self):
        self.ThreadActive = True
        print("Starting Camera Feed...")

        self.getCameraMatrix()

        while self.ThreadActive:
            _, self.frame = self.cap.read()

            if _:
                #Get OpenCV Image
                self.Face.setImgFrame(self.frame)
                faces = self.Face.getFaces()

                for face in faces:
                    if self.showFaceTrack:
                        self.displayFaceTrack(face, self.frame)

                    if self.showLandmarks:
                        landmarks = self.Face.getLandmarks(face)
                        self.displayLandmarks(landmarks, self.frame)

                    if self.showPose:
                        landmarks = self.Face.getLandmarks(face)
                        end_point2D = self.poseEstimation(self.frame)

                        p1 = ( landmarks.part(34-1).x, landmarks.part(34-1).y) #todo: get nose
                        p2 = ( int(end_point2D[0][0][0]), int(end_point2D[0][0][1]))

                        cv2.line(self.frame, p1, p2, (0,0,255), 2)
                        
                    if self.showNose:
                        landmarks = self.Face.getLandmarks(face)
                        self.displayNose(self.frame, landmarks)

                RGB_Image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(RGB_Image, 1)

                #Convert to Qt Image
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
            
    def stop(self):
        self.ThreadActive = False
        self.quit()

    def setSFT(self, bFlag):
        self.showFaceTrack = bFlag

    def setSL(self, bFlag):
        self.showLandmarks = bFlag

    def setSN(self, bFlag):
        self.showNose = bFlag

    def setSP(self, bFlag):
        self.showPose = bFlag

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


class Media_Worker(Camera_Worker):

    def run(self):
        self.path = ""
        self.setMediaPath("./data/video.mp4")
        self.ThreadActive = True
        print("Starting media player...")
        cap = cv2.VideoCapture(self.path)

        if (cap.isOpened()== False):
            print("Error: Could not read video file.")

        while(cap.isOpened() and self.ThreadActive == True):
            #capture frame by frame
            _, self.frame = cap.read()
            if _:

                #Get OpenCV Image
                self.Face.setImgFrame(self.frame)
                faces = self.Face.getFaces()

                for face in faces:
                    if self.showFaceTrack:
                        self.displayFaceTrack(face, self.frame)

                    if self.showLandmarks:
                        landmarks = self.Face.getLandmarks(face)
                        self.displayLandmarks(landmarks, self.frame)

                    if self.showPose:
                        landmarks = self.Face.getLandmarks(face)
                        end_point2D = self.poseEstimation(self.frame)

                        p1 = ( landmarks.part(34-1).x, landmarks.part(34-1).y) #todo: get nose
                        p2 = ( int(end_point2D[0][0][0]), int(end_point2D[0][0][1]))

                        cv2.line(self.frame, p1, p2, (0,0,255), 2)
                        
                    if self.showNose:
                        landmarks = self.Face.getLandmarks(face)
                        self.displayNose(self.frame, landmarks)

                RGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                #Convert to Qt Image
                ConvertToQtFormat = QImage(RGB.data, RGB.shape[1], RGB.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    
    def setMediaPath(self, path):
        self.path = path

    def stop(self):
        self.ThreadActive = False
        self.quit()