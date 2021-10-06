# CAVE_FacialMoCap
Continuing personal investigation into markerless facial motion capture techniques using consumer technologies and free open source software

- [CAVE_FacialMoCap](#cave_facialmocap)
  - [Overview](#overview)
  - [Background](#background)
  - [Build & Run](#build--run)
    - [Dependencies](#dependencies)
    - [Other Libraries Used (Optional)](#other-libraries-used-optional)
  - [Usage](#usage)
  - [Supported Platforms](#supported-platforms)
  - [Implementation](#implementation)
  - [Future Work](#future-work)
  - [References](#references)

## Overview
An experimental pipeline was developed to drive the facial animationof a Metahuman rig in real-time using Unreal Engine 4.27. The system takes a single RGB source from a live camera stream or stored video file and leverages computer vision libraries to detect a human face. The motion of key facial features can then be sent to the game engine instance and mapped to animation Blueprints which were originally designed to take data from the Live Link Face app.

By removing the need for depth data from a device with a TrueDepth camera, this project opens up the possibility for live puppeteering of complex digital avatars without having to buy into the closed ecosystem of high-end Apple devices.

## Background


## Build & Run
### Dependencies
* Unreal Engine 4.27: [Release Notes/Download](https://www.unrealengine.com/en-US/release-notes/unreal-engine-4-27-released)
* TCP Plugin for UE4.27: [Github](https://github.com/CodeSpartan/UE4TcpSocketPlugin)[Unreal Marketplace](https://unrealengine.com/marketplace/en-US/product/tcp-socket-plugin)
* `PyQt`: [https://pypi.org/project/PyQt5/](https://pypi.org/project/PyQt5/)
* `OpenCV`: [https://opencv.org/](https://opencv.org/)
* `dlib`: [http://dlib.net/](http://dlib.net/)

### Other Libraries Used (Optional)
* `PyQt3D`: [https://pypi.org/project/PyQt3D/](https://pypi.org/project/PyQt3D/)
* `eos`: [https://github.com/patrikhuber/eos](https://github.com/patrikhuber/eos)
* `Mediapipe`: [https://google.github.io/mediapipe/](https://google.github.io/mediapipe/)

## Usage
###*To Run Python GUI:*
1. Clone or download git repository
2. Install dependencies listed in README if not already
3. Download and unzip **Resources.zip** provided separately
4. Add files from *Resources/data* into *CAVE_FacialMocap/data*
5. Run `facial_mocap.py`

###*To Run Unreal Project:*
1. Install Unreal Engine 4.27
2. To use my MH, add **Georgie_FaceMesh.uasset** from provided Resources and move into Content folder under *CAVE_FacialMocap/UE4.27/Faces/Content/MetaHumans/Georgie/Face/*

## Supported Platforms
Tested on MacOS with Python 3.?

Tested on Windows 10 with Python 3.?

## Implementation

## Future Work


## References
1.