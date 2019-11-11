import pyrealsense2 as rs
import numpy as np
import time
import cv2

cam_X = 640
cam_Y = 480
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, cam_X, cam_Y, rs.format.z16, 60)
config.enable_stream(rs.stream.color, cam_X, cam_Y, rs.format.bgr8, 60) #60

pipeline.start(config)

# Frame timer for FPS display
fps = 0
frame_counter = 0
frame_counter_start = time.time()

while True:
    # Read BGR frame
    
    frames = pipeline.wait_for_frames()
    frame = frames.get_color_frame()
    
    depth_frame = frames.get_depth_frame()
    frame = np.asanyarray(frame.get_data())
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame_counter += 1

    if frame_counter % 10 == 0:
        frame_counter_end = time.time()
        fps = int(10 / (frame_counter_end - frame_counter_start))
        frame_counter = 0
        frame_counter_start = time.time()
    cv2.putText(frame, f"FPS: {fps}", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

    cv2.imshow("jou",frame)
    if cv2.waitKey(5) & 0xFF == ord("q"):
            break
