# -*- coding: utf-8 -*-
import cv2
import numpy as np


def BallTracking(image, block_pix):
    thre_area = 2500
    height, width, _ = image.shape
    # image = image[80:height, :]
    # convert bgr to hsv
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges for tennis balls
    colors = {
        # 'pink': ([162, 151, 188], [177, 224, 254]),
        # 'yellow': ([29, 200, 141], [34, 234, 234]),
        # 'orange': ([4, 153, 157], [7, 247, 236]),
        # 'red': ([0, 234,  58], [4, 255, 151]),
        # 'green': ([59, 186, 122], [66, 252, 198]),
        'real green': ([30, 114, 92], [50, 233, 255])
    }


    # Create masks and apply morphology operations
    masks = {}
    for color, (lower, upper) in colors.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        # kernel = np.ones((15, 15), np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        masks[color] = mask
        # cv2.imshow('1', mask)

    # Search for circular contours in each mask and stop after finding one
    largest_contour = None
    largest_contour_area = 0
    for color, mask in masks.items():
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > largest_contour_area and area > thre_area:
                    largest_contour_area = area
                    largest_contour = contour
        if largest_contour_area > thre_area:
            print(largest_contour_area)
            break
        else:
            largest_contour = None

    # Draw bounding circle around the largest contour if found
    if largest_contour is not None:
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(image, center, radius, (0, 255, 0), 2)
        if center[1] > block_pix:
            return True, image, center

    # If no circular contours are found, return False
    return False, None, None
