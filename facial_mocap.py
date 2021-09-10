# [1] Qt5/OpenCV window code modified from:
# https://www.codepile.net/pile/ey9KAnxn
# [2] Face landmark detection code modified from:
# https://pysource.com/2019/03/12/face-landmarks-detection-opencv-with-python/
# [3] Head pose estimation code modified from:
# https://learnopencv.com/head-pose-estimation-using-opencv-and-dlib/
# (See P.I. submission for full references for this section ^)


#todo:
# handle if camera not detected - warning

from face_prediction import ShapePredictor
from viewer import MainWindow
from PyQt5.QtWidgets import *

import sys
#import mediapipe as mp

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())
