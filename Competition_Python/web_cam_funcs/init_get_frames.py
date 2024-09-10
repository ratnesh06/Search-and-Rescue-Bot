import cv2
import platform

def get_camera_serial_number(camera_index):
    # Use the AVFoundation flag to access the camera
    cap = cv2.VideoCapture(camera_index + cv2.CAP_AVFOUNDATION)

    # Check if the camera is opened
    if cap.isOpened():
        # Get camera properties
        properties = {}
        for i in range(10):  # Assuming 10 properties max
            prop = cap.get(i)
            properties[i] = prop

        # Get serial number if available
        serial_number = properties.get(5)  # Assuming property 5 corresponds to serial number
        if serial_number:
            print("Camera {} serial number: {}".format(camera_index, serial_number))
            return serial_number
        else:
            print("Camera {} serial number not available.".format(camera_index))

        cap.release()
    else:
        print("Failed to open camera {}".format(camera_index))

def check_all_cameras(max_index, obj_serial):
    # Try to get the serial number of all possible cameras
    for index in range(max_index):
        serial = get_camera_serial_number(index)
        if obj_serial in str(serial):
            return index

def count_connected_cameras():
    num_cameras = 0
    index = 0
    while True:
        # Try to open the next camera index
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            print('num_cam: {}', num_cameras)
            break
        num_cameras += 1
        cap.release()
        index += 1

    return num_cameras

def InitCam(width, height):

    cap = cv2.VideoCapture(0)
    cap.set(3, width)  # width
    cap.set(4, height)  # height
    return cap

def ObtainBGRFrame(cap):
    grabbed, BGRimage = cap.read()
    return grabbed, BGRimage


