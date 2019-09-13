import cv2
import time
import vision
import config
import processes
import main

import robot_movement


def start(processes_variables):
    movement = robot_movement.Movement()
    stop = processes_variables[3]
    right_wheel = processes_variables[0]
    middle_wheel = processes_variables[1]
    left_wheel = processes_variables[2]

    right_wheel_angle = 120
    middle_wheel_angle = 0
    left_wheel_angle = 240

    device = config.get("vision", "video_capture_device")
    cap = cv2.VideoCapture(device)
    



    # Frame timer for FPS display
    fps = 0
    frame_counter = 0
    frame_counter_start = time.time()


    while cap.isOpened():
        
        if stop:
            break
            # Read BGR frame
        _, frame = cap.read()

        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # TODO: find ball coordinates in filtered image
        ball_color_mask, basket_color_mask, ball_coords, basket_coords = vision.apply_ball_color_filter(hsv)

        centerX = frame.shape[1]/2
        print("Center: ", centerX, " ball_coords: ", ball_coords[0])


        """
        right_wheel_angle = 120
        middle_wheel_angle = 0
        left_wheel_angle = 240
        """
        if (ball_coords[0] < centerX + 80) and (ball_coords[0] > centerX - 80):
            processes_variables[0] = 0
            processes_variables[1] = 0
            processes_variables[2] = 0

        else:
            #Check movement.py.calculate_linear_velocity
            print(movement.calculate_linear_velocity(centerX,ball_coords[0], 1, 8, right_wheel_angle, 120))
            processes_variables[0] = movement.calculate_linear_velocity(centerX,ball_coords[0], 1, 20, right_wheel_angle, 90)
            processes_variables[1] = movement.calculate_linear_velocity(centerX,ball_coords[0], 1, 20, middle_wheel_angle, 90)
            processes_variables[2] = movement.calculate_linear_velocity(centerX,ball_coords[0], 1, 20, left_wheel_angle, 90)

        # Handle keyboard input
        key = cv2.waitKey(1)

        if key & 0xFF == ord("q"):

            break

        # FPS display

        frame_counter += 1

        if frame_counter % 10 == 0:
            frame_counter_end = time.time()
            fps = int(10 / (frame_counter_end - frame_counter_start))
            frame_counter = 0
            frame_counter_start = time.time()

        cv2.putText(frame, str(fps), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        cv2.putText(frame, str(int(ball_coords[0]))+" "+str(int(ball_coords[1])), (int(ball_coords[0]), int(ball_coords[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))

        cv2.putText(frame, str(int(basket_coords[0]))+" "+str(int(basket_coords[1])), (int(basket_coords[0]), int(basket_coords[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 266, 0))

        total_img = cv2.bitwise_or(ball_color_mask, basket_color_mask)

        # Show frame
        cv2.imshow("frame", frame)
        cv2.imshow("ball_color", ball_color_mask)
        cv2.imshow("basket color", basket_color_mask)
        cv2.imshow("combined", total_img)

    # Exit cleanly
    cap.release()
    cv2.destroyAllWindows()
