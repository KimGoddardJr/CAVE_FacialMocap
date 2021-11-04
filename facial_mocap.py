"""
MSc Project - Georgie Challis (s5400010), 2021 
Facial animation from webcam data to Unreal Engine.

Dependencies:
* OpenCV
* PySide2
* dlib

See individual modules for code references and resources
See written report for academic references and theory
"""
import sys
from enum import Enum
from PySide2 import QtWidgets

from modules.viewer import MainWindow

#Global Variables
#Operation modes:
class Mode(Enum):
    GUI_ONLY = 0 #Just display the face tracking
    GUI_GEOM = 1 #Display face tracking and mask geometry (py)
    TCP_ONLY = 2 #Data transport via TCP (no OSC)
    IMS_FULL = 3 #Data transport via IMS Live Link Plugin

bShowGeomPreview = False

if __name__ == "__main__":
    import sys

    App = QtWidgets.QApplication(sys.argv)
    Root = MainWindow(Mode.TCP_ONLY)
    #Main GUI:
    Root.show()
    #Preview geometry window
    if bShowGeomPreview:
        Root.Show()
    sys.exit(App.exec_())
