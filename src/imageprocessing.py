import cv2
import time
import vision
import config
import processes
import main
import numpy as np
import pyrealsense2 as rs
from robot_movement import calculate_linear_velocity as linear_mvmt


def turnToFindTheBall(processes_variables, ballInCenter, middle_x_pixel=None, ball_X=None, ball_Y=None, basket_X=None, basket_Y=None):
    right_wheel_angle = 120
    middle_wheel_angle = 0
    left_wheel_angle = 240
    wheel_speed = 20
    movement_direction_forward = 90

    """
    If ball is in center, move forward
    else turn around its axis and find the ball
    """
    if ballInCenter:
        print(ballInCenter, "BALLINCENTER")
        #right wheel
        processes_variables[0] = int(linear_mvmt(-wheel_speed, right_wheel_angle, movement_direction_forward, middle_x_pixel, ball_X, ball_Y))
        processes_variables[1] = int(linear_mvmt(wheel_speed, middle_wheel_angle, movement_direction_forward, middle_x_pixel, ball_X, ball_Y))
        processes_variables[2] = int(linear_mvmt(-wheel_speed, left_wheel_angle, movement_direction_forward, middle_x_pixel, ball_X, ball_Y))

        if ball_Y > 350:
            processes_variables[0] = 0
            processes_variables[1] = -30
            processes_variables[2] = 0
            if (basket_X < middle_x_pixel + 20) and (basket_X > middle_x_pixel - 20):
                processes_variables[0] = -20
                processes_variables[1] = 0
                processes_variables[2] = 20
                time.sleep(1)
                processes_variables[4] = 1
                time.sleep(1)
                



    else:
        print(ballInCenter, "BALL EI TOHIKS OLLA CENTRIS")
        processes_variables[0] = wheel_speed
        processes_variables[1] = wheel_speed
        processes_variables[2] = wheel_speed


def start(processes_variables):
    
    
    cam_X = 640
    cam_Y = 480
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, cam_X, cam_Y, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, cam_X, cam_Y, rs.format.bgr8, 60)

    pipeline.start(config)
    
    distances = np.zeros(10)
    center_x_avg_array = [cam_X/2 for _ in range(10)]
    center_y_avg_array = [cam_Y/2 for _ in range(10)]
    # Frame timer for FPS display
    fps = 0
    frame_counter = 0
    frame_counter_start = time.time()

    asd = True

    # Array for the current ball we're chasing (to reduce noise in blob detection)
    # We take the mean x and y of the last 5 "balls" we've detected and see the deviation from that for
    # The current ball, so if we get noise in a random place, we are not likely to follow that
    #cap = cv2.VideoCapture(2)

    while True:
        stop = processes_variables[3]
        if stop:
            break

        # Read BGR frame
        
        frames = pipeline.wait_for_frames()
        frame = frames.get_color_frame()
        depth_image = frames.get_depth_frame()
        frame = np.asanyarray(frame.get_data())
        
        if asd:
            processes_variables[0] = -10
            processes_variables[2] = 10
            time.sleep(3)
            asd = False

        #_, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        ball_x, ball_y, ball_r, mask_ball = vision.apply_ball_color_filter(hsv, basket=False)
        basket_x, basket_y, basket_r, mask_basket = vision.apply_ball_color_filter(hsv, basket=True)
        ball_x = int(ball_x)
        ball_y = int(ball_y)
        ball_r = int(ball_r)
        cv2.circle(frame, (ball_x, ball_y), ball_r, (0,255,0),1)
        basket_x = int(basket_x)
        basket_y = int(basket_y)
        basket_r = int(basket_r)
        cv2.circle(frame, (basket_x, basket_y), basket_r, (0,0,255),1)

        centerX = frame.shape[1]/2

        center_x_avg_array.pop(0); center_x_avg_array.append(ball_x)
        ball_x = int(np.median(center_x_avg_array))

        center_y_avg_array.pop(0); center_y_avg_array.append(ball_y)
        ball_y = int(np.median(center_y_avg_array))
        #CHANGED

        if (ball_x < centerX + 160) and (ball_x > centerX - 160):
            print(ball_x, "BALL ball_X")
            print(centerX, "center ball_X")
            ballInCenter = True
            turnToFindTheBall(processes_variables, ballInCenter, centerX, ball_x, ball_y, basket_x, basket_y)

        else:
            ballInCenter = False
            print(ball_x, "BALL ball_X")
            print(centerX, "center ball_X")
            turnToFindTheBall(processes_variables, ballInCenter, centerX, ball_x, ball_y, basket_x, basket_y)

        
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
        
        cv2.putText(frame, str(fps), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        #cv2.putText(frame, f"d: {meanDistToBasket}", (ball_x, ball_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        cv2.putText(frame, f"{ball_x} {ball_y}", (ball_x, ball_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))
        #cv2.putText(frame, f"{basket_x} {basket_y}", (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0))


        # Show frame
        cv2.imshow("Raw", frame)
        cv2.imshow("Masked", mask_ball)

    # Exit cleanly


    pipeline.stop()
    #cap.release()
    cv2.destroyAllWindows()
