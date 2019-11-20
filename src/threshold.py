import cv2
from functools import partial
import config
import numpy as np
import pyrealsense2 as rs

"""blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByInertia = False
blobparams.filterByColor = False
blobparams.filterByCircularity = False
blobparams.filterByArea = False
blobparams.filterByConvexity = False


detector = cv2.SimpleBlobDetector_create(blobparams)"""

def apply_ball_color_filter(hsv, ball_color_range, params):

    """
    hsv = cv2.medianBlur(hsv, 5)
    mask_ball = cv2.inRange(hsv, ball_color_range["min"], ball_color_range["max"])
    kernel = np.ones((2,2), np.uint8)  # 11
    #mask_ball = cv2.Canny(mask_ball, 100, 300)
    mask_ball = cv2.morphologyEx(mask_ball, cv2.MORPH_OPEN, kernel)
    erosion = cv2.erode(mask_ball, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=2)
    cont, hie = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)"""

    #hsv = cv2.blur(hsv, (2,2))
    mask_ball = cv2.inRange(hsv, ball_color_range["min"], ball_color_range["max"])
    kernel = np.ones((5,5), np.uint8)
    masked_img = cv2.morphologyEx(mask_ball, cv2.MORPH_OPEN, kernel)
    erosion = cv2.erode(masked_img, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    #dilation = masked_img
    cont, hie = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow("VAATA SEDA", dilation)

    """
    blobparams.minCircularity = params["circ"][0]
    blobparams.maxCircularity = params["circ"][1]
    blobparams.minArea = params["area"][0]
    blobparams.maxArea = params["area"][1]
    blobparams.minConvexity = params["conv"][0]
    blobparams.maxConvexity = params["conv"][1]
    detector = cv2.SimpleBlobDetector_create(blobparams)

    coords_ball = detector.detect(mask_ball)
    """
    # Only return the blob of the largest objects of the same color
    return cont


def start():
    # Ask for color name to threshold
    color_name = input("Enter color name: ")

    # Try to get saved range from config file, use whole color space as default if not saved
    # Color ranges are saved as { "min": (hmin, smin, vmin), "max": (hmax, smax, vmax) }
    color_range = config.get("colors", color_name, default={ "min": (0, 0, 0), "max": (179, 255, 255) })
    params = config.get("blobparams", "params", default={'circ': (0, 1), 'area': (0, 1), 'conv': (0, 1)})
    # Create trackbars (sliders) for HSV channels
    cv2.namedWindow("frame")

    def update_range(i, j, value):
        values = list(color_range[i])
        values[j] = value
        color_range[i] = tuple(values)
    def update_params(i, j, value):
        values = list(params[i])
        if i != "area":
            values[j] = value/100
        else:
            values[j] = value*100
        params[i] = tuple(values)
    cv2.createTrackbar("h_min", "frame", color_range["min"][0], 179, partial(update_range, "min", 0))
    cv2.createTrackbar("s_min", "frame", color_range["min"][1], 255, partial(update_range, "min", 1))
    cv2.createTrackbar("v_min", "frame", color_range["min"][2], 255, partial(update_range, "min", 2))
    cv2.createTrackbar("h_max", "frame", color_range["max"][0], 179, partial(update_range, "max", 0))
    cv2.createTrackbar("s_max", "frame", color_range["max"][1], 255, partial(update_range, "max", 1))
    cv2.createTrackbar("v_max", "frame", color_range["max"][2], 255, partial(update_range, "max", 2))
    cv2.createTrackbar("circ_min", "frame", params["circ"][0], 100, partial(update_params, "circ", 0))
    cv2.createTrackbar("area_min", "frame", params["area"][0], 500, partial(update_params, "area", 0))
    cv2.createTrackbar("conv_min", "frame", params["conv"][0], 100, partial(update_params, "conv", 0))
    #cv2.createTrackbar("circ_max", "frame", params["circ"][1], 100, partial(update_params, "circ", 1))
    #cv2.createTrackbar("area_max", "frame", params["area"][1], 500, partial(update_params, "area", 1))
    #cv2.createTrackbar("conv_max", "frame", params["conv"][1], 100, partial(update_params, "conv", 1))

    # Capture camera
    device = config.get("vision", "video_capture_device")
    #cap = cv2.VideoCapture(device)
    pipeline = rs.pipeline()
    config1 = rs.config()
    config1.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
    config1.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

    pipeline.start(config1)
    while 1:
        # Read BGR frame
        frames = pipeline.wait_for_frames()
        frame = frames.get_color_frame()
        depth_image = frames.get_depth_frame()
        bgr = np.asanyarray(frame.get_data())

        # Convert to HSV
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

        # Apply color mask to HSV image
        mask = cv2.inRange(hsv, color_range["min"], color_range["max"])

        cont = apply_ball_color_filter(hsv, color_range, params)
        cv2.drawContours(bgr, cont, -1, (0, 255, 255), 1)


        """for ball in balls:
            ball_coords = ball.pt
            ball_x = int(ball_coords[0])
            ball_y = int(ball_coords[1])
            cv2.putText(bgr, f"{ball_x} {ball_y}", (ball_x, ball_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255))
"""
        # Display filtered image
        cv2.imshow("mask", mask)
        cv2.imshow("frame", bgr)
        

        # Handle keyboard input
        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

    # Overwrite color range
    config.set("colors", color_name, color_range)
    for key in params:
        vals = list(params[key])
        for i, val in enumerate(vals):
            if key != "area":
                vals[i] = int(val*100)
            else:
                vals[i] = val
        params[key] = tuple(vals)

    config.set("blobparams", "params", params)
    config.save()

    # Exit cleanly
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start()
