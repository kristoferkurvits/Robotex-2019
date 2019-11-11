import cv2
import pyrealsense2 as rs
import numpy as np
from threading import Thread

class imageCapRS2:
    def commandThread(self):
        while self.running:
            frames = self.pipeline.wait_for_frames()
            self.depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            self.currentFrame = np.asanyarray(color_frame.get_data())
    def __init__(self, src=0):
        self.running = True
        self.depth_frame = None
        self.currentFrame = None
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
        self.pipeline.start(self.config)
        Thread(name="commandThread", target=self.commandThread).start()

    def getFrame(self):
        return self.depth_frame, self.currentFrame