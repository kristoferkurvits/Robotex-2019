import cv2
from functools import partial
import config

import numpy as np
blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByInertia = False
blobparams.filterByColor = False
blobparams.filterByCircularity = True
blobparams.minCircularity = 0.85
blobparams.maxCircularity = 1
blobparams.filterByArea = True
blobparams.minArea = 30 #75
blobparams.maxArea = 50000
blobparams.filterByConvexity = True
blobparams.minConvexity = 0.7
blobparams.maxConvexity = 1
detector = cv2.SimpleBlobDetector_create(blobparams)

def apply_ball_color_filter(hsv, ball_color_range):
    hsv = cv2.medianBlur(hsv, 5)
    mask_ball = cv2.inRange(hsv, ball_color_range["min"], ball_color_range["max"])
    kernel = np.ones(3)  # 11
    mask_ball = cv2.morphologyEx(mask_ball, cv2.MORPH_OPEN, kernel)

    coords_ball = detector.detect(mask_ball)

    # Only return the blob of the largest objects of the same color
    largest_ball_size = 0
    largest_ball_coords = [0, 0]
    for keypoint in coords_ball:
        if keypoint.size > largest_ball_size:
            largest_ball_size = keypoint.size
            largest_ball_coords = keypoint.pt

    return (mask_ball, largest_ball_coords)


def start():
    # Ask for color name to threshold
    color_name = input("Enter color name: ")

    # Try to get saved range from config file, use whole color space as default if not saved
    # Color ranges are saved as { "min": (hmin, smin, vmin), "max": (hmax, smax, vmax) }
    color_range = config.get("colors", color_name, default={ "min": (0, 0, 0), "max": (179, 255, 255) })

    # Create trackbars (sliders) for HSV channels
    cv2.namedWindow("frame")

    def update_range(i, j, value):
        values = list(color_range[i])
        values[j] = value
        color_range[i] = tuple(values)

    cv2.createTrackbar("h_min", "frame", color_range["min"][0], 179, partial(update_range, "min", 0))
    cv2.createTrackbar("s_min", "frame", color_range["min"][1], 255, partial(update_range, "min", 1))
    cv2.createTrackbar("v_min", "frame", color_range["min"][2], 255, partial(update_range, "min", 2))
    cv2.createTrackbar("h_max", "frame", color_range["max"][0], 179, partial(update_range, "max", 0))
    cv2.createTrackbar("s_max", "frame", color_range["max"][1], 255, partial(update_range, "max", 1))
    cv2.createTrackbar("v_max", "frame", color_range["max"][2], 255, partial(update_range, "max", 2))

    # Capture camera
    device = config.get("vision", "video_capture_device")
    cap = cv2.VideoCapture(device)

    while cap.isOpened():
        # Read BGR frame
        _, bgr = cap.read()

        # Convert to HSV
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

        # Apply color mask to HSV image
        mask = cv2.inRange(hsv, color_range["min"], color_range["max"])

        ball_color_mask, ball_coords = apply_ball_color_filter(hsv, color_range)


        ball_x = int(ball_coords[0])
        ball_y = int(ball_coords[1])

        cv2.putText(bgr, f"{ball_x} {ball_y}", (ball_x, ball_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))
        cv2.imshow("masked", cv2.bitwise_and(bgr, bgr, mask=ball_color_mask))
        # Display filtered image
        cv2.imshow("frame", bgr)

        # Handle keyboard input
        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

    # Overwrite color range
    config.set("colors", color_name, color_range)
    config.save()

    # Exit cleanly
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start()
