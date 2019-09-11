import cv2
import time
import vision
import config
import processes
import main

should_stop = False

def stop():
    global should_stop

    return should_stop

def start(Robo_serial):
    global should_stop
    # optional TOOD: capture frames on separate thread
    # Capture camera
    device = config.get("vision", "video_capture_device")
    cap = cv2.VideoCapture(device)
    


    #hi
    # Frame timer for FPS display
    fps = 0
    frame_counter = 0
    frame_counter_start = time.time()

    while cap.isOpened():
        # Read BGR frame
        _, frame = cap.read()

        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # TODO: find ball coordinates in filtered image
        ball_color_mask, basket_color_mask, ball_coords, basket_coords = vision.apply_ball_color_filter(hsv)

        centerX = frame.shape[1]/2

        if (ball_coords[0] < centerX + 40) and (ball_coords[0] > centerX - 40):
            Robo_serial[0] = 0
        else:
            Robo_serial[0] = 15
        
        # Handle keyboard input
        key = cv2.waitKey(1)

        if key & 0xFF == ord("q"):
            should_stop = True
            print("imgprocess", should_stop)
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
