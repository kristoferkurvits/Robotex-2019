import cv2
import numpy as np
from threading import currentThread
import config


# TODO: display errors when configuration file is missing any of these values
# Get color ranges and noise removal kernels from config
ball_color_range = config.get("colors", config.get("vision", "ball_color"))
ball_noise_kernel = config.get("vision", "ball_noise_kernel")
basket_color_range = config.get("colors", config.get("vision", "basket_color"))

# Get boolean image with ball color filter applied
def apply_ball_color_filter(hsv):
    # Apply ball color filter
    mask_ball = cv2.inRange(hsv, ball_color_range["min"], ball_color_range["max"])
    mask_basket = cv2.inRange(hsv, basket_color_range["min"], basket_color_range["max"])
    # TODO: Remove noise (Google opencv morphological transformations)

    return (mask_ball, mask_basket)

# TODO: blob detection for balls and baskets
