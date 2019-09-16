import cv2
import numpy as np
from threading import currentThread
import config

blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByInertia = False
blobparams.filterByColor = False
blobparams.filterByCircularity = False
blobparams.filterByArea = True
blobparams.minArea = 50
blobparams.maxArea = 50000
blobparams.filterByConvexity = False
detector = cv2.SimpleBlobDetector_create(blobparams)

# Get color ranges and noise removal kernels from config
ball_color_range = config.get("colors", config.get("vision", "ball_color"))
ball_noise_kernel = config.get("vision", "ball_noise_kernel")
basket_color_range = config.get("colors", config.get("vision", "basket_color"))

def apply_ball_color_filter(hsv):

    """
        args: 
            hsv image
        returns: 
            1) masked image of the ball
            2) masked image of the basket
            3) [x, y] for the coordinates of the ball
            4) [x, y] for the coordinates of the basket
    """

    hsv = cv2.medianBlur(hsv, 5)
    mask_ball = cv2.inRange(hsv, ball_color_range["min"], ball_color_range["max"])
    mask_basket = cv2.inRange(hsv, basket_color_range["min"], basket_color_range["max"])
    kernel = np.ones(11)
    mask_ball = cv2.morphologyEx(mask_ball, cv2.MORPH_OPEN, kernel)
    mask_basket = cv2.morphologyEx(mask_basket, cv2.MORPH_OPEN, kernel)

    coords_ball = detector.detect(mask_ball)
    coords_basket = detector.detect(mask_basket)

    # Only return the blob of the largest objects of the same color
    largest_ball_size = 0
    largest_ball_coords = [0, 0]
    for keypoint in coords_ball:
        if keypoint.size > largest_ball_size:
            largest_ball_size = keypoint.size
            largest_ball_coords = keypoint.pt

    largest_basket_size = 0
    largest_basket_coords = [0, 0]
    for keypoint in coords_basket:
        if keypoint.size > largest_basket_size:
            largest_basket_size = keypoint.size
            largest_basket_coords = keypoint.pt

    return (mask_ball, mask_basket, largest_ball_coords, largest_basket_coords)


