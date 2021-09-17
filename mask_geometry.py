#!/usr/bin/env python
"""
This is a Python port of Qt 3D: Simple C++ Example code
https://doc.qt.io/qt-5.10/qt3d-simple-cpp-example.html

pip install PyQt5 (Version 5.10)
"""

import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt3DCore import *
from PyQt5.Qt3DExtras import *
from PyQt5.QtWidgets import *


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
        self.childEntity = QEntity(self.rootEntity)
        #sphere
        self.mesh = QSphereMesh()
        self.mesh.setRadius(5)

    def createScene(self):
        objectTransform = QTransform()
        controller = OrbitTransformController(objectTransform)
        controller.setTarget(objectTransform)
        controller.setRadius(10)

        objectRotateTransformAnimation = QPropertyAnimation(objectTransform)
        objectRotateTransformAnimation.setTargetObject(controller)
        objectRotateTransformAnimation.setPropertyName(b'angle')
        objectRotateTransformAnimation.setStartValue(0)
        objectRotateTransformAnimation.setEndValue(360)
        objectRotateTransformAnimation.setDuration(10000)
        objectRotateTransformAnimation.setLoopCount(-1)
        objectRotateTransformAnimation.start()

        self.childEntity.addComponent(self.mesh)
        self.childEntity.addComponent(objectTransform)
        self.childEntity.addComponent(self.material)

        return self.rootEntity

#Run module on its own to test widget
if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = Qt3DWindow()
    demo = demo_Scene()
    scene_3d = demo.createScene()

    # Camera
    camera = view.camera()
    camera.lens().setPerspectiveProjection(45.0, 16.0/9.0, 0.1, 1000.0)
    camera.setPosition(QVector3D(0, 0, 40.0))
    camera.setViewCenter(QVector3D(0, 0, 0))

    # For camera controls
    camController = QOrbitCameraController(scene_3d)
    camController.setLinearSpeed( 50.0 )
    camController.setLookSpeed( 180.0 )
    camController.setCamera(camera)

    view.setRootEntity(scene_3d)
    view.show()

    sys.exit(app.exec_())