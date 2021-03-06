import cv2
import time
import vision
import config
import processes
import main
import numpy as np
import pyrealsense2 as rs
from scipy import ndimage
from robot_movement import calculate_linear_velocity as linear_mvmt
from robot_movement import move
import matplotlib.pyplot as plt


def turnToFindTheBall(processes_variables, ballInCenter, basket_distance, middle_x_pixel=None, ball_X=None, ball_Y=None, basket_X=None, basket_Y=None):
    right_wheel_angle = 120
    middle_wheel_angle = 0
    left_wheel_angle = 240
    wheel_speed = 20
    movement_direction_forward = 90

    """
    If ball is in center, move forward
    else turn around its axis and find the ball
    """

    move(processes_variables, ballInCenter, basket_distance, middle_x_pixel, ball_X, ball_Y, basket_X, basket_Y)

def start(processes_variables):
    auto = 1
    
    cam_X = 640
    cam_Y = 480
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, cam_X, cam_Y, rs.format.z16, 60)
    config.enable_stream(rs.stream.color, cam_X, cam_Y, rs.format.bgr8, 60) #60

    pipeline.start(config)
    
    center_basket_avg_array = [1.5 for _ in range(12)] #metres
    # Frame timer for FPS display
    fps = 0
    frame_counter = 0
    frame_counter_start = time.time()


    # Array for the current ball we're chasing (to reduce noise in blob detection)
    # We take the mean x and y of the last 5 "balls" we've detected and see the deviation from that for
    # The current ball, so if we get noise in a random place, we are not likely to follow that
    #cap = cv2.VideoCapture(2)
    processes_variables[0] = -75
    processes_variables[1] = 0
    processes_variables[2] = 75
    time.sleep(1.6)
    while True:
        

        # Read BGR frame
        
        frames = pipeline.wait_for_frames()
        frame = frames.get_color_frame()
        
        depth_frame = frames.get_depth_frame()
        frame = np.asanyarray(frame.get_data())
        
        #frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        #depth_image = np.asanyarray(depth_frame.get_data())
        #frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        #frame = ndimage.rotate(frame, 270)
        #frame = np.transpose(frame)

        #_, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        
        ball_x, ball_y, ball_r, mask_ball = vision.apply_ball_color_filter(hsv, basket=False)
        basket_x, basket_y, basket_r, mask_basket = vision.apply_ball_color_filter(hsv, basket=True)
        
        if ball_x != None:
            cv2.circle(frame, (ball_x, ball_y), ball_r, (0,255,0),1)
        
        if basket_x != None:
            basket_distance = round(depth_frame.get_distance(basket_x, basket_y), 2)
            center_basket_avg_array.pop(0); center_basket_avg_array.append(basket_distance)
            cv2.circle(frame, (basket_x, basket_y), basket_r, (0,0,255),1)
            processes_variables[3] = np.mean(center_basket_avg_array)
        else:
            basket_distance = -1
        
        centerX = frame.shape[1]/2 + 18 # enne 18

        #CHANGED
        if auto:
            #if (ball_x < centerX + 160) and (ball_x > centerX - 160):
            if (ball_x != None):
                #print(ball_x, "BALL ball_X")
                #print(centerX, "center ball_X")
                ballInCenter = True
                turnToFindTheBall(processes_variables, ballInCenter, basket_distance, centerX, ball_x, ball_y, basket_x, basket_y)

            else:
                ballInCenter = False
                #print(ball_x, "BALL ball_X")
                #print(centerX, "center ball_X")
                turnToFindTheBall(processes_variables, ballInCenter, basket_distance, centerX, ball_x, ball_y, basket_x, basket_y)

        
        #CHANGED

        # Handle keyboard input
        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

        # FPS display
        frame_counter += 1

        if frame_counter % 10 == 0:
            frame_counter_end = time.time()
            fps = int(10 / (frame_counter_end - frame_counter_start))
            frame_counter = 0
            frame_counter_start = time.time()
        """
        distanceToBasket = depth_image.get_distance(int(basket_x), int(basket_y))
        distances = np.append(distances, round(distanceToBasket, 3))
        distances = np.delete(distances, 0)
        meanDistToBasket = round(np.mean(distances), 3)
        """
        
        
        

        #cv2.putText(frame, f"d: {meanDistToBasket}", (ball_x, ball_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        if ball_x != None:
            cv2.putText(frame, f"{ball_x} {ball_y}", (ball_x, ball_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))
        #cv2.putText(frame, f"{basket_x} {basket_y}", (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0))

        # info frame
        info_frame = np.zeros_like(frame)
        if ball_x != None:
            ball_diff_str = f"Ball diff: {cam_X/2-ball_x}"
        else:
            ball_diff_str = "No ball"
        if basket_x != None:
            basket_diff_str = f"Basket diff: {cam_X/2-basket_x+20}"
        else:
            basket_diff_str = "No basket"

        basket_distance_str = f"Basket dist: {basket_distance}"
        cv2.putText(info_frame, f"FPS: {fps}", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        cv2.putText(info_frame, ball_diff_str, (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        cv2.putText(info_frame, basket_diff_str, (5, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        cv2.putText(info_frame, basket_distance_str, (5, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        # Show frame
        cv2.line(frame, (int(centerX), 0), (int(centerX), cam_Y), (255, 255, 255), 2)
        if basket_x != None:
            cv2.line(frame, (int(basket_x), int(basket_y)), (int(basket_x), int(basket_y)), (150, 150, 0), 9)
        frame = np.concatenate([frame, info_frame], axis=1)
        cv2.imshow("Raw", frame)
        #cv2.imshow("Depth", depth_image)
        #cv2.imshow("Masked", mask_ball)
        #print("FPS: ", fps)

    # Exit cleanly


    pipeline.stop()
    #cap.release()
    cv2.destroyAllWindows()
