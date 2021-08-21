# modified from pythonforthelab.com/blog/step-by-step-guide-to-building-a-gui/
import cv2

class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None
    
    def initialise(self):
        self.cap = cv2.VideoCapture(self.cam_num)

    def get_frame(self):
        pass

    def acquire_movie(self, num_frames):
        movie = []
        for n in range(num_frames):
            movie.append(self.get_frame())
        return movie
    
    def set_brightness(self, value):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    def get_brightness(self):
        self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

    def get_frame(self):
        __, self.last_frame = self.cap.read()
        return self.last_frame

    def close_camera(self):
        self.cap.release()

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)

if __name__ == '__main__':
    cam = Camera(0)
    cam.initialise()
    print(cam)
    frame = cam.get_frame()
    print(frame)
    cam.close_camera()