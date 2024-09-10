from web_cam_funcs import init_get_frames, ball_tracking_v2
import cv2
img_width = 640
img_height = 480
cap = init_get_frames.InitCam(img_width, img_height)
while True:
    grabbed, BGRimage = init_get_frames.ObtainBGRFrame(cap)
    if not grabbed:
        break
    if_tracked, tracked_image, center_point = ball_tracking_v2.BallTracking(BGRimage)
    if if_tracked:
        cv2.imshow('tracked_image', tracked_image)
        print(center_point)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break