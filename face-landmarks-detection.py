'''
https://pysource.com/2019/03/12/face-landmarks-detection-opencv-with-python/
https://learnopencv.com/head-pose-estimation-using-opencv-and-dlib/

'''


import cv2
import numpy as np
import dlib

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

numLandmarks = 68
chin = 9
nose = 34
left_eye = 37
right_eye = 46
left_mouth = 49
right_mouth = 55

def displayLandmarks(frame, landmarks, face):
    
    for n in range(0, numLandmarks):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)

def displayNose(frame, ladnmarks, face):
    x = landmarks.part(nose-1).x
    y = landmarks.part(nose-1).y
    cv2.circle(frame, (x, y), 4, (255, 255, 255), -1)

def displayFaceTrack():
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        #displayFaceTrack()

        landmarks = predictor(gray, face)

        #displayLandmarks(frame, landmarks, face)
        displayNose(frame,landmarks,face)

        #2D capture points:
        cap_points = np.array([
                                (landmarks.part(nose-1).x, landmarks.part(nose-1).y),     
                                (landmarks.part(chin-1).x, landmarks.part(chin-1).y),     # Chin
                                (landmarks.part(left_eye-1).x, landmarks.part(left_eye-1).y),     # Left eye left corner
                                (landmarks.part(right_eye-1).x, landmarks.part(right_eye-1).y),     # Right eye right corne
                                (landmarks.part(left_mouth-1).x, landmarks.part(left_mouth-1).y),     # Left Mouth corner
                                (landmarks.part(right_mouth-1).x, landmarks.part(right_mouth-1).y)      # Right mouth corner
                            ], dtype="double")

        # 3D model points.
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

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
