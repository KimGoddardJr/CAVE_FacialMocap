from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


from modules.face_prediction import *


class Idle(QThread):
    ImageUpdate = pyqtSignal(QImage)
    Face = None
    frame = None
    width = 0
    height = 0

    def run(self):
        self.ThreadActive = True
        while True:
            #Set black image
            Image = QPixmap(560,480)
            Image.fill(Qt.black)
            self.ImageUpdate.emit(Image)

    def stop(self):
        self.ThreadActive = False
        self.quit()

class Camera_Worker(Idle):
    Face = SP_68points()

    #Get feed from camera 0
    cap = cv2.VideoCapture(0)

    #Display option flags
    bShowFaceTrack = False
    bShowLandmarks = False
    bShowNose = False
    bShowPose = False
    bExportFile = False
    bExportImg = False

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
                    if self.bShowFaceTrack:
                        self.displayFaceTrack(face, self.frame)

                    if self.bShowLandmarks:
                        landmarks = self.Face.getLandmarks(face)
                        self.displayLandmarks(landmarks, self.frame)

                    if self.bShowPose:
                        landmarks = self.Face.getLandmarks(face)
                        end_point2D = self.poseEstimation(self.frame)

                        p1 = ( landmarks.part(34-1).x, landmarks.part(34-1).y) #todo: get nose properly
                        p2 = ( int(end_point2D[0][0][0]), int(end_point2D[0][0][1]))

                        cv2.line(self.frame, p1, p2, (0,0,255), 2)
                        
                    if self.bShowNose:
                        landmarks = self.Face.getLandmarks(face)
                        self.displayNose(self.frame, landmarks)

                RGB_Image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(RGB_Image, 1)

                #Convert to Qt Image
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
            

    def setSFT(self, bFlag):
        self.bShowFaceTrack = bFlag

    def setSL(self, bFlag):
        self.bShowLandmarks = bFlag

    def setSN(self, bFlag):
        self.bShowNose = bFlag

    def setSP(self, bFlag):
        self.bShowPose = bFlag

    def setFileExport(self, bFlag):
        self.bExportFile = bFlag
    
    def setImgExport(self, bFlag):
        self.bExportImg = bFlag

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
        bLines = True
        for n in range(0, 67): #todo: update numLandmarks
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 3, (255, 0, 0), -1)

            dont_connect = [16, 21, 26, 35, 41, 47, 67]
            if bLines:
                if n not in dont_connect:
                    p0 = (landmarks.part(n).x,landmarks.part(n).y)
                    p1 = (landmarks.part(n+1).x,landmarks.part(n+1).y)
                    cv2.line(frame, p0, p1, (200,0,55), 2)
                #close nose triangle
                p0 = (landmarks.part(30).x,landmarks.part(30).y)
                p1 = (landmarks.part(35).x,landmarks.part(35).y)
                cv2.line(frame, p0, p1, (200,0,55), 2)

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

    def stop(self):
        self.ThreadActive = False
        self.quit()


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
                    if self.bShowFaceTrack:
                        self.displayFaceTrack(face, self.frame)

                    if self.bShowLandmarks:
                        landmarks = self.Face.getLandmarks(face)
                        self.displayLandmarks(landmarks, self.frame)

                    if self.bShowPose:
                        landmarks = self.Face.getLandmarks(face)
                        end_point2D = self.poseEstimation(self.frame)

                        p1 = ( landmarks.part(34-1).x, landmarks.part(34-1).y) #todo: get nose
                        p2 = ( int(end_point2D[0][0][0]), int(end_point2D[0][0][1]))

                        cv2.line(self.frame, p1, p2, (0,0,255), 2)
                        
                    if self.bShowNose:
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

