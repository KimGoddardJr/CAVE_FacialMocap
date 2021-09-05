
# [2] Face landmark detection code modified from:
# https://pysource.com/2019/03/12/face-landmarks-detection-opencv-with-python/
# [3] Head pose estimation code modified from:
# https://learnopencv.com/head-pose-estimation-using-opencv-and-dlib/
# (See P.I. submission for full references)

import cv2
import numpy as np
import dlib

from datetime import datetime

fileOutputEnabled = True

class ShapePredictor:
    def __init__(self):
        #set init time
        self.initTime=datetime.now()

        # identify key landmarks for face direction
        self.numLandmarks = 68
        self.chin = 9
        self.nose = 34
        self.left_eye = 37
        self.right_eye = 46
        self.left_mouth = 49
        self.right_mouth = 55

        # 3D model points (taken from [3])
        self.model_points = np.array([
                            (0.0, 0.0, 0.0),             # Nose tip
                            (0.0, -330.0, -65.0),        # Chin
                            (-225.0, 170.0, -135.0),     # Left eye left corner
                            (225.0, 170.0, -135.0),      # Right eye right corne
                            (-150.0, -150.0, -125.0),    # Left Mouth corner
                            (150.0, -150.0, -125.0)      # Right mouth corner
                        ])

        self.landmarks = None

        # Camera
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
        self.landmarks = self.predictor(self.Grey_Image, face)
        return self.landmarks

    def getCapPoints(self, camera_matrix, distortion):
        
        cap_points = np.array([
                            (self.landmarks.part(self.nose-1).x, self.landmarks.part(self.nose-1).y),     
                            (self.landmarks.part(self.chin-1).x, self.landmarks.part(self.chin-1).y),     # Chin
                            (self.landmarks.part(self.left_eye-1).x, self.landmarks.part(self.left_eye-1).y),     # Left eye left corner
                            (self.landmarks.part(self.right_eye-1).x, self.landmarks.part(self.right_eye-1).y),     # Right eye right corne
                            (self.landmarks.part(self.left_mouth-1).x, self.landmarks.part(self.left_mouth-1).y),     # Left Mouth corner
                            (self.landmarks.part(self.right_mouth-1).x, self.landmarks.part(self.right_mouth-1).y)      # Right mouth corner
                        ], dtype="double")

        if fileOutputEnabled:
            #Writes as----> Runtime: nose.x,nose.y chin.x,chin.y ....etc
            date = self.initTime.strftime("%d-%m-%Y")
            fileDescription = "6features_" + date + ".txt"
            file = open(fileDescription, "a")

            file.write(str(datetime.now()-self.initTime))
            file.write(": ")
            for p in cap_points:
                point = str(p[0]) + ","  + str(p[1]) + '\t'
                file.write(point)
            
            file.write('\n')
            file.close()

        #SolvePnP for camera 
        (success, rotation_vector, translation_vector) = cv2.solvePnP(self.model_points, 
                                                                cap_points, 
                                                                camera_matrix, 
                                                                distortion, 
                                                                flags=cv2.SOLVEPNP_ITERATIVE
                                                            )

        (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), 
                                                                    rotation_vector, 
                                                                    translation_vector, 
                                                                    camera_matrix,
                                                                    distortion
                                                        )

        return nose_end_point2D

class MP_ShapePredictor(ShapePredictor):
    #For implementation of mediapipe landmarks instead
    pass