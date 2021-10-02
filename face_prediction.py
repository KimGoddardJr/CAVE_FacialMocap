# [2] Face landmark detection code modified from:
# https://pysource.com/2019/03/12/face-landmarks-detection-opencv-with-python/
# [3] Head pose estimation code modified from:
# https://learnopencv.com/head-pose-estimation-using-opencv-and-dlib/
# [4] Rotation vector->Matrix Conversion taken from:
# https://learnopencv.com/rotation-matrix-to-euler-angles/ 

# (See P.I. submission for full references)

import cv2
import dlib
import numpy as np
import math

from datetime import datetime

fileOutputEnabled = True



class ShapePredictorBase:
    def __init__(self):
        #set init time
        self.initTime=datetime.now()

        # identify key landmarks for face direction
        self.numLandmarks = 0
        self.landmarks = None

        self.detector = None
        self.predictor = None
        self.cap_points = None

        # Camera
        self.frame = None
        self.Grey_Image = None
        self.cap_points = np.array([])
        self.model_points = np.array([])

        #Set to true once initial head rotation (euler) is found
        self.initialRotation = np.zeros(3)
        self.initialRotationSet = False

    def setImgFrame(self, frame):
        self.Grey_Image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def getFaces(self):
        #Run Face Detection
        faces = self.detector(self.Grey_Image)
        return faces

    def getLandmarks(self, face):
        #Get Facial Landmarks
        self.landmarks = self.predictor(self.Grey_Image, face)
        self.writePts()
        return self.landmarks

    def getCapPoints(self, camera_matrix, distortion):
        self.cap_points = np.array([
            (self.landmarks.part(self.nose-1).x, self.landmarks.part(self.nose-1).y),
            (self.landmarks.part(self.chin-1).x, self.landmarks.part(self.chin-1).y),     # Chin
            (self.landmarks.part(self.left_eye-1).x, self.landmarks.part(self.left_eye-1).y),     # Left eye left corner
            (self.landmarks.part(self.right_eye-1).x, self.landmarks.part(self.right_eye-1).y),     # Right eye right corne
            (self.landmarks.part(self.left_mouth-1).x, self.landmarks.part(self.left_mouth-1).y),     # Left Mouth corner
            (self.landmarks.part(self.right_mouth-1).x, self.landmarks.part(self.right_mouth-1).y)      # Right mouth corner
        ], dtype="double")

        #SolvePnP for camera
        (success, rotation_vector, translation_vector) = cv2.solvePnP(self.model_points,
                                                                self.cap_points,
                                                                camera_matrix,
                                                                distortion,
                                                                flags=cv2.SOLVEPNP_ITERATIVE
        )

        #Rotation vec to matrix
        rotation_matrix = np.zeros((3,3))
        rotation_euler = np.zeros(3)
        cv2.Rodrigues(rotation_vector, rotation_matrix)
        rotation_euler = rotationMatrixToEulerAngles(rotation_matrix)

        if not self.initialRotationSet:
            self.initialRotation = rotation_euler
            self.initialRotationSet = True

        new_rotation = rotation_euler-self.initialRotation
        print(new_rotation)

        #Project back to 2D
        (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]),
                                                                    rotation_vector,
                                                                    translation_vector,
                                                                    camera_matrix,
                                                                    distortion
        )
        return nose_end_point2D

    def writePts(self):
        if fileOutputEnabled:
            #Writes as----> Run-time: nose.x,nose.y chin.x,chin.y ....etc
            date = self.initTime.strftime("%d-%m-%Y")
            fileDescription = "landmarks_" + date + ".pts"
            file = open(fileDescription, "w")

            #file.write(str(datetime.now()-self.initTime))
            file.write("version: 1\n")
            file.write("n_points: %d\n" %self.numLandmarks)
            file.write('{\n')
            for i in range (0, self.numLandmarks):
                x = self.landmarks.part(i).x
                y = self.landmarks.part(i).y
                point = str(x) + " "  + str(y) + '\n'
                file.write(point)
            file.write('}\n')
            file.close()

    def saveCropped(self, img, x, y, w, h):
        bbox_scale = 1.05
        #todo face_img = img[y:y+h, x:x+w]
        #     cv2.imwrite('frame.png', face_img)


class SP_68points(ShapePredictorBase):
    def __init__(self):
        super().__init__()
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

        # shape_predictor_68_face_landmarks.dat file must be in same directory
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("./data/shape_predictor_68_face_landmarks.dat")

class SP_81points(SP_68points):
    def __init__(self):
        #set init time
        self.initTime=datetime.now()

        # identify key landmarks for face direction
        self.numLandmarks = 81

        # 3D model points (taken from [3])
        self.model_points = np.array([
                            (0.0, 0.0, 0.0),             # Nose tip
                            (0.0, -330.0, -65.0),        # Chin
                            (-225.0, 170.0, -135.0),     # Left eye left corner
                            (225.0, 170.0, -135.0),      # Right eye right corne
                            (-150.0, -150.0, -125.0),    # Left Mouth corner
                            (150.0, -150.0, -125.0)      # Right mouth corner
        ])

        # shape_predictor_68_face_landmarks.dat file must be in same directory
        self.detector = dlib.get_frontal_face_detector()
        #self.predictor = dlib.shape_predictor("shape_predictor_81_face_landmarks.dat")

class SP_Mediapipe(ShapePredictorBase):
    #For implementation of mediapipe landmarks instead
    pass





#Utility functions
 #From https://learnopencv.com/rotation-matrix-to-euler-angles/ -------------
# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R) :

    assert(isRotationMatrix(R))

    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])

    singular = sy < 1e-6

    if  not singular :
        x = math.degrees(math.atan2(R[2,1] , R[2,2]))
        y = math.degrees(math.atan2(-R[2,0], sy))
        z = math.degrees(math.atan2(R[1,0], R[0,0]))
    else :
        x = math.degrees(math.atan2(-R[1,2], R[1,1]))
        y = math.degrees(math.atan2(-R[2,0], sy))
        z = 0

    return np.array([x, y, z])

  #-------