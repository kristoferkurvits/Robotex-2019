import cv2
import time
import vision
import config
import processes
import main
import numpy as np
import pyrealsense2 as rs
from robot_movement import calculate_linear_velocity as linear_mvmt


def turnToFindTheBall(processes_variables, ballInCenter, middle_x_pixel=None, X=None, Y=None):
    right_wheel_angle = 120
    middle_wheel_angle = 0
    left_wheel_angle = 240
    wheel_speed = 10
    movement_direction_forward = 90

    """
    If ball is in center, move forward
    else turn around its axis and find the ball
    """
    if ballInCenter:
        print(ballInCenter, "BALLINCENTER")
        #right wheel
        processes_variables[0] = int(linear_mvmt(-wheel_speed, right_wheel_angle, movement_direction_forward, middle_x_pixel, X, Y))
        processes_variables[1] = int(linear_mvmt(wheel_speed, middle_wheel_angle, movement_direction_forward, middle_x_pixel, X, Y))
        processes_variables[2] = int(linear_mvmt(-wheel_speed, left_wheel_angle, movement_direction_forward, middle_x_pixel, X, Y))

    else:
        print(ballInCenter, "BALL EI TOHIKS OLLA CENTRIS")
        processes_variables[0] = wheel_speed
        processes_variables[1] = wheel_speed
        processes_variables[2] = wheel_speed

    
def start(processes_variables):

    

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline.start(config)
    distances = np.zeros(10)
    
    # Frame timer for FPS display
    fps = 0
    frame_counter = 0
    frame_counter_start = time.time()

    while True:
        stop = processes_variables[3]
        if stop:
            break

        # Read BGR frame
        frames = pipeline.wait_for_frames()
        frame = frames.get_color_frame()
        depth_image = frames.get_depth_frame()
        frame = np.asanyarray(frame.get_data())

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        ball_color_mask, basket_color_mask, ball_coords, basket_coords = vision.apply_ball_color_filter(hsv)

        centerX = frame.shape[1]/2

        ball_x = int(ball_coords[0])
        ball_y = int(ball_coords[1])
        basket_x = int(basket_coords[0])
        basket_y = int(basket_coords[1])


        #CHANGED

        
        if (ball_x < centerX + 160) and (ball_x > centerX - 160):
            print(ball_x, "BALL X")
            print(centerX, "center X")
            ballInCenter = True
            turnToFindTheBall(processes_variables, ballInCenter, centerX, ball_x, ball_y)

        else:
            ballInCenter = False
            print(ball_x, "BALL X")
            print(centerX, "center X")
            turnToFindTheBall(processes_variables, ballInCenter, centerX, ball_x, ball_y)

        
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

        distanceToBasket = depth_image.get_distance(int(basket_x), int(basket_y))
        distances = np.append(distances, round(distanceToBasket, 3))
        distances = np.delete(distances, 0)
        meanDistToBasket = round(np.mean(distances), 3)

        
        cv2.putText(frame, str(fps), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        cv2.putText(frame, f"d: {meanDistToBasket}", (ball_x, ball_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        cv2.putText(frame, f"{ball_x} {ball_y}", (ball_x, ball_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))
        cv2.putText(frame, f"{basket_x} {basket_y}", (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0))

        total_img = cv2.bitwise_or(ball_color_mask, basket_color_mask)

        # Show frame
        cv2.imshow("Raw", frame)
        cv2.imshow("Combined img", total_img)

    # Exit cleanly


    pipeline.stop()
    #cap.release()
    cv2.destroyAllWindows()
