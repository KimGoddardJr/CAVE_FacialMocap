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

def displayLandmarks(frame, gray, face):
    landmarks = predictor(gray, face)
    
    for n in range(0, numLandmarks):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)

def displayNose(frame, gray, face):
    landmarks = predictor(gray, face)
    x = landmarks.part(nose-1).x
    y = landmarks.part(nose-1).y
    cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)

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

        #displayLandmarks(frame, gray, face)
        #displayFaceTrack()
        displayNose(frame,gray,face)


    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
