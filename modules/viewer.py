# Qt5/OpenCV window code modified from: https://www.codepile.net/pile/ey9KAnxn

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

try:
    from PyQt5.Qt3DCore import *
    from PyQt5.Qt3DExtras import *
except:
    print("PyQt3D not found")

import numpy as np

from modules.mask_geometry import *
from modules.input_stream import *
import modules.data_export

#Display option flags
showFaceTrack = False
showLandmarks = False
showNose = False
showPose = False

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.streamEnabled = False
        self.mediaEnabled = False
        self.CurrentThread = None
        self.DataRecording = False

        #Window
        title = "OpenCV Face Mocap [WIP] - s5400010"
        self.setWindowTitle(title)

        self.layout = QHBoxLayout()
        #self.layout.addWidget(container)

        self.SetUpUI()

        Image = QPixmap(640,480)
        Image.fill(Qt.black)
        self.FeedLabel.setPixmap(Image)

        # Child layout to Window
        self.setLayout(self.layout)


    def Show(self):
        #3D Window to Widget
        self.view = Qt3DWindow()
        scene = demo_Scene()
        demo = scene.createScene()
        # Camera
        camera = self.view.camera()
        camera.lens().setPerspectiveProjection(45.0, 16.0/9.0, 0.1, 1000.0)
        camera.setPosition(QVector3D(0, 0, 40.0))
        camera.setViewCenter(QVector3D(0, 0, 0))
        self.view.setRootEntity(demo)
        self.view.defaultFrameGraph().setClearColor(QColor("#4d4d4f"))
        self.container = self.createWindowContainer(self.view)
        self.container.show()

    def SetUpUI(self):

        #Placeholders for input/output widgets displayed
        self.FeedLabel = QLabel()
        self.layout.addWidget(self.FeedLabel)

        #Buttons
        self.buttonsGB = QGroupBox("Display Options")
        self.VBL = QVBoxLayout()

        self.csLabel = QLabel()
        self.VBL.addWidget(self.csLabel)
        self.csLabel.setText("Face Input Method:")

        self.camSelect = QComboBox()
        self.camSelect.addItems(["None", "Webcam", "Media"])
        self.camSelect.currentIndexChanged.connect(self.SelectInput)
        self.VBL.addWidget(self.camSelect)

        verticalSpacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.VBL.addItem(verticalSpacer)

        self.ToggleFaceLoc = QPushButton("Show/Hide Face Track")
        self.ToggleFaceLoc.clicked.connect(self.TglFaceLoc)
        self.VBL.addWidget(self.ToggleFaceLoc)

        self.ToggleLandmarks = QPushButton("Show/Hide Landmarks")
        self.ToggleLandmarks.clicked.connect(self.TglLandmarks)
        self.VBL.addWidget(self.ToggleLandmarks)

        self.Toggle3DPose = QPushButton("Show Pose Estimation")
        self.Toggle3DPose.clicked.connect(self.TglPose)
        self.VBL.addWidget(self.Toggle3DPose)

        verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.VBL.addItem(verticalSpacer)

        #Change path to media file:
        self.pathLabel = QLabel("Path to media file:")
        self.VBL.addWidget(self.pathLabel)

        self.pathEdit = QLineEdit("./data/video.mp4")
        self.pathEdit.setReadOnly(True)
        self.pathEdit.setEnabled(False)
        self.VBL.addWidget(self.pathEdit)

        verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.VBL.addItem(verticalSpacer)

        self.CancelBtn = QPushButton("Start Data Record")
        self.CancelBtn.clicked.connect(self.TglDataExport)
        self.VBL.addWidget(self.CancelBtn)

        self.enableFile = QCheckBox("Write to File")
        self.enableFile.setChecked(False)
        self.enableFile.setCheckable(False)
        self.enableFile.toggled.connect(self.TglFile)
        self.VBL.addWidget(self.enableFile)

        self.enableImg = QCheckBox("Write to Image")
        self.enableImg.setChecked(False)
        self.enableImg.setCheckable(False)
        self.enableImg.toggled.connect(self.TglImage)
        self.VBL.addWidget(self.enableImg)

        self.buttonsGB.setLayout(self.VBL)
        self.layout.addWidget(self.buttonsGB)
        
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def TglImage(self):
        itemClicked = self.sender()
        self.CurrentThread.setFileExport(itemClicked.checkState())

    def TglFile(self):
        itemClicked = self.sender()
        self.CurrentThread.setFileExport(itemClicked.checkState())

    def SelectInput(self):
        newIndex = self.camSelect.currentIndex()
        if self.streamEnabled or self.mediaEnabled == True:
            self.CurrentThread.stop()
            print("Stopped running thread....")
        if newIndex == 2: #play from file
            print("Input: Media")
            self.streamEnabled = False
            self.mediaEnabled = True
            self.CurrentThread = Media_Worker()
            #Pass on button settings from GUI
            self.CurrentThread.setSFT(showFaceTrack)
            self.CurrentThread.setSL(showLandmarks)
            self.CurrentThread.setSP(showPose)
            #Enable checkboxes
            self.enableFile.setCheckable(True)
            self.enableImg.setCheckable(True)
            self.pathEdit.setEnabled(True)
        elif newIndex == 1:
            print("Input: Webcam")
            self.streamEnabled = True
            self.mediaEnabled = False
            self.CurrentThread = Camera_Worker()
            #Pass on button settings from GUI
            self.CurrentThread.setSFT(showFaceTrack)
            self.CurrentThread.setSL(showLandmarks)
            self.CurrentThread.setSP(showPose)
            #Enable Checkboxes
            self.enableFile.setCheckable(True)
            self.enableImg.setCheckable(True)
            self.pathEdit.setEnabled(False)
        else:
            print("Input: None") 
            self.streamEnabled = False
            self.mediaEnabled = False

            #Disable checkbox
            self.enableFile.setCheckable(False)
            self.enableImg.setCheckable(False)
            self.pathEdit.setEnabled(False)
            return

        self.CurrentThread.ImageUpdate.connect(self.ImageUpdateSlot)
        self.CurrentThread.start()
          
    def TglDataExport(self):
        print("Exporting data...")
        self.DataRecording = not self.DataRecording
        #todo: If true, start recording
        if self.DataRecording:
            self.CancelBtn.setText("Stop Recording")
        else:
            self.CancelBtn.setText("Start Recording")
        #todo: If false, stop recording
        pass

    def TglFaceLoc(self):
        if self.streamEnabled or self.mediaEnabled:
            global showFaceTrack
            showFaceTrack = not showFaceTrack
            self.CurrentThread.setSFT(showFaceTrack)

    def TglLandmarks(self):
        if self.streamEnabled or self.mediaEnabled:
            global showLandmarks 
            showLandmarks = not showLandmarks
            self.CurrentThread.setSL(showLandmarks)

    def TglPose(self):
        if self.streamEnabled or self.mediaEnabled:
            global showPose
            showPose = not showPose
            self.CurrentThread.setSP(showPose)
    

