import cv2
import time
import vision
import config
import processes
import main
import robot_movement.calculate_linear_velocity as linear_mvmt

def start(processes_variables):

    right_wheel_angle = 120
    middle_wheel_angle = 0
    left_wheel_angle = 240

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline.start(config)
    should_stop = False
    distances = np.zeros(10)
    
    # Frame timer for FPS display
    fps = 0
    frame_counter = 0
    frame_counter_start = time.time()

    while 1:
        stop = processes_variables[0]
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

        if (ball_coords[0] < centerX + 80) and (ball_coords[0] > centerX - 80):
            processes_variables[0] = 0
            processes_variables[1] = 0
            processes_variables[2] = 0

        else:
            #Check movement.py.calculate_linear_velocity
            processes_variables[0] = linear_mvmt(centerX,ball_coords[0], 1, 20, right_wheel_angle, 90)
            processes_variables[1] = linear_mvmt(centerX,ball_coords[0], 1, 20, middle_wheel_angle, 90)
            processes_variables[2] = linear_mvmt(centerX,ball_coords[0], 1, 20, left_wheel_angle, 90)

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
        
        ball_x = int(ball_coords[0])
        ball_y = int(ball_coords[1])
        basket_x = int(basket_coords[0])
        basket_y = int(basket_coords[1])

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
    cap.release()
    cv2.destroyAllWindows()
