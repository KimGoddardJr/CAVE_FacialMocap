#!/usr/bin/env python
"""
Python port of Qt 3D: Simple C++ Example code
https://doc.qt.io/qt-5.10/qt3d-simple-cpp-example.html
"""
import eos
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

try:
    from PyQt5.Qt3DCore import *
    from PyQt5.Qt3DExtras import *
    from PyQt5.Qt3DRender import *
except:
    print("PyQt3D not found.")


class OrbitTransformController(QObject):
    def __init__(self, parent):
        super(OrbitTransformController, self).__init__(parent)
        self.m_target = QTransform()
        self.m_matrix = QMatrix4x4()
        self.m_radius = 1.0
        self.m_angle = 0

    def getTarget(self):
        return self.m_target

    def setTarget(self, target):
        if self.m_target != target:
            self.m_target = target
            self.targetChanged.emit()

    def getRadius(self):
        return self.m_radius

    def setRadius(self, radius):
        if not QtCore.qFuzzyCompare(self.m_radius, radius):
            self.m_radius = radius
            self.updateMatrix()
            self.radiusChanged.emit()

    def getAngle(self):
        return self.m_angle

    def setAngle(self, angle):
        if not QtCore.qFuzzyCompare(angle, self.m_angle):
            self.m_angle = angle
            self.updateMatrix()
            self.angleChanged.emit()

    def updateMatrix(self):
        self.m_matrix.setToIdentity()
        self.m_matrix.rotate(self.m_angle, QVector3D(0, 1, 0))
        self.m_matrix.translate(self.m_radius, 0, 0)
        self.m_target.setMatrix(self.m_matrix)

    # QSignal
    targetChanged = pyqtSignal()
    radiusChanged = pyqtSignal()
    angleChanged = pyqtSignal()

    # Qt properties
    target = pyqtProperty(QTransform, fget=getTarget, fset=setTarget)
    radius = pyqtProperty(float, fget=getRadius, fset=setRadius)
    angle = pyqtProperty(float, fget=getAngle, fset=setAngle)


class demo_Scene():
    def __init__(self):
        self.rootEntity = QEntity()
        self.material = QPhongMaterial(self.rootEntity)

        #sphere
        self.mesh = QMesh()
        url = QUrl()
        url.setScheme("file")
        url.setPath("data/mp_facegeometry2.obj")
        self.mesh.setSource(url)

    def createScene(self):
        objectTransform = QTransform()
        controller = OrbitTransformController(objectTransform)
        controller.setTarget(objectTransform)

        self.rootEntity.addComponent(self.mesh)
        self.rootEntity.addComponent(objectTransform)
        self.rootEntity.addComponent(self.material)

        return self.rootEntity

"""
EOS Lightweight 3DMM demo from:
https://github.com/patrikhuber/eos/blob/master/python/demo.py
"""

def get_3dmm():
    """Demo for running the eos fitting from Python."""
    landmarks = read_pts('./data/image_0010.pts')
    image_width = 1280 # Make sure to adjust these when using your own images!
    image_height = 1024

    model = eos.morphablemodel.load_model("./data/sfm_shape_3448.bin")
    blendshapes = eos.morphablemodel.load_blendshapes("./data/expression_blendshapes_3448.bin")
    # Create a MorphableModel with expressions from the loaded neutral model and blendshapes:
    morphablemodel_with_expressions = eos.morphablemodel.MorphableModel(model.get_shape_model(), blendshapes,
                                                                        color_model=eos.morphablemodel.PcaModel(),
                                                                        vertex_definitions=None,
                                                                        texture_coordinates=model.get_texture_coordinates())
    landmark_mapper = eos.core.LandmarkMapper('./data/ibug_to_sfm.txt')
    edge_topology = eos.morphablemodel.load_edge_topology('./data/sfm_3448_edge_topology.json')
    contour_landmarks = eos.fitting.ContourLandmarks.load('./data/ibug_to_sfm.txt')
    model_contour = eos.fitting.ModelContour.load('./data/sfm_model_contours.json')

    (mesh, pose, shape_coeffs, blendshape_coeffs) = eos.fitting.fit_shape_and_pose(morphablemodel_with_expressions,
        landmarks, landmark_mapper, image_width, image_height, edge_topology, contour_landmarks, model_contour)

    # Now you can use your favourite plotting/rendering library to display the fitted mesh, using the rendering
    # parameters in the 'pose' variable.

    # Or for example extract the texture map, like this:
    # import cv2
    # image = cv2.imread('.//data/image_0010.png')
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA, 4)  # extract_texture(...) expects a 4-channel image
    # texturemap = eos.render.extract_texture(mesh, pose, image)


def read_pts(filename):
    """A helper function to read the 68 ibug landmarks from a .pts file."""
    lines = open(filename).read().splitlines()
    lines = lines[3:71]

    landmarks = []
    ibug_index = 1  # count from 1 to 68 for all ibug landmarks
    for l in lines:
        coords = l.split()
        landmarks.append(eos.core.Landmark(str(ibug_index), [float(coords[0]), float(coords[1])]))
        ibug_index = ibug_index + 1

    return landmarks


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        title = "OpenCV Face Mocap [WIP] - s5400010"
        self.setWindowTitle(title)

        lay = QVBoxLayout(self)
        self.view = Qt3DWindow()
        container = QWidget.createWindowContainer(self.view)
        lay.addWidget(container)
        scene = demo_Scene()
        scene.createScene()
        self.rootEntity = scene
        cameraEntity = self.view.camera()
        camController = QFirstPersonCameraController(scene.rootEntity)
        camController.setCamera(cameraEntity)
        self.view.setRootEntity(scene.rootEntity)

#Run module on its own to test widget
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Root = MainWindow()

    view = Qt3DWindow()

    demo = demo_Scene()
    scene_3d = demo.createScene()
    # Camera
    camera = view.camera()
    camera.lens().setPerspectiveProjection(45.0, 16.0/9.0, 0.1, 1000.0)
    camera.setPosition(QVector3D(0, 0, 50.0))
    camera.setViewCenter(QVector3D(0, 0, 0))

    view.setRootEntity(scene_3d)
    view.show()

    sys.exit(app.exec_())
    

