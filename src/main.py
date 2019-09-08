import cv2
import time
import vision
import config


def start():
    # optional TOOD: capture frames on separate thread
    # Capture camera
    device = config.get("vision", "video_capture_device")
    cap = cv2.VideoCapture(2)

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
        ball_color_mask, basket_color_mask = vision.apply_ball_color_filter(hsv)

        # TODO: also detect opponent basket
        # TODO: run AI
        # optional TODO: run AI on separate thread
        
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

        total_img = cv2.bitwise_or(ball_color_mask, basket_color_mask)

        # Show frame
        cv2.imshow("frame", frame)
        cv2.imshow("ball_color", ball_color_mask)
        cv2.imshow("basket color", basket_color_mask)
        cv2.imshow("combined", total_img)

    # Exit cleanly
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start()
