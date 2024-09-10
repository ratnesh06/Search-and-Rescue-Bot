import cv2  # state of the art computer vision algorithms library

from lidar_funcs import open_close_cp2102
from arduino_com_func import connect_ard
from web_cam_funcs import init_get_frames, ball_tracking_v2
from strategy import ball_pick, PID_wall_following
import time

if __name__ == '__main__':
    # init, start program
    window_size = 3
    data_store_f = []
    data_store_l = []
    data_store_r = []
    forward_dist_1 = []
    left_dist_1 = []
    right_dist_1 = []
    uturn_threth = 500
    exit_threth = 1200

    # init cam
    img_width = 500
    img_height = 480
    block_pix = 80
    cap = init_get_frames.InitCam(img_width, img_height)
    if cap:
        print('cam opened')

    # init arduino
    ser_ard = []
    open_series = 1
    is_open, ser_ard = connect_ard.ConnArd(open_series, ser_ard)
    if is_open:
        print("Arduino port {} is open".format(ser_ard.name))
    else:
        print("Arduino port is not open")

    # wait for init
    time.sleep(2)

    # start loop
    '''
    Wall following (no ball found): follow the right wall, if front distance is small (wall a head), tank turn left.
    if front distance is not too large but the right distance is too large, fully turn right because of the door
    if the front distance is too large and the left distance is too large, stop
    Ball tracking (ball found): Follow and pick the ball up, if the door is open, just go straight until the door is closed
    '''
    ball_count = 0
    currenttime = time.time()
    force_wall_follow = 0
    while True:
        # get distances from Arduino by sonar
        while True:  # loop until get correct data
            try:
                sonar_ball_data = ser_ard.readline().decode().strip()
                if sonar_ball_data:
                    values = sonar_ball_data.split(',')
                    if len(values) == 4:
                        sonar_ball_data = [int(value) for value in values]
                        '''
                        Serial.print(sonar_r);
              Serial.print(",");
              Serial.print(sonar_l);
              Serial.print(",");
              Serial.print(sonar_f);
              Serial.print(",");
              Serial.println(ball_count);
                        '''
                        right_dist_1 = sonar_ball_data[0]
                        left_dist_1 = sonar_ball_data[1]
                        forward_dist_1 = sonar_ball_data[2]
                        ball_count = sonar_ball_data[3]
                        if forward_dist_1 != []:
                            forward_dist = forward_dist_1
                        if left_dist_1 != []:
                            left_dist = left_dist_1
                        if right_dist_1 != []:
                            right_dist = right_dist_1
                        break
            except:
                pass

        print('front: {}'.format(ball_count))
        print('left:{}'.format(left_dist))
        print('right:{}'.format(right_dist))
        
        # print(right_dist)
        # Wall Following, max_speed = 1


        turn_mode, PID_left_right = PID_wall_following.RightWallFollowing(distance_front=forward_dist,
                                                                          distance_left=left_dist,
                                                                          distance_right=right_dist,
                                                                          uturn_threth=uturn_threth,
                                                                          exit_threth=exit_threth)
        max_speed = 1  # full speed during wall following
        servo_pos = 0  # close door during wall following
        wall_follow = 1  # 1 wall following, 0 pick ball;

        if ball_count < 3:  # when collected 3 balls, only wall following
            # get track from web cam
            grabbed, BGRimage = init_get_frames.ObtainBGRFrame(cap)
            #cv2.imshow('BGRimage', BGRimage)
            if not grabbed:
                continue
            if_tracked, tracked_image, center_point = ball_tracking_v2.BallTracking(BGRimage, block_pix)
            if if_tracked: # and min(forward_dist, left_dist, right_dist) > 150:
                print('ball tracked')
                #cv2.imshow('track ball', tracked_image)
                PID_left_right = ball_pick.TrackBall(center_point)  # [-1,1]
                percent_speed, servo_pos = ball_pick.SpeedCloseBallandPick(center_point)
                max_speed = percent_speed
                wall_follow = 0
            elif servo_pos == 1:
                max_speed = 0.1  # move slowly to collect the ball
                turn_mode = 1
                PID_left_right = 0
                wall_follow = 0
            grabbed = 0
            if_tracked = 0
            del tracked_image
            del BGRimage

        if cv2.waitKey(1) == ord("q"):
            break

        '''
        data structure: servo position (0 init or 1 open or -1 dont care from python); 
        turn mode (-1 tank turn sig, 0 stop sig, 1 normal turn sig);
        turning control sig (PID: -1 left, 0 straight forward,1 right);(if tank turn, -1 left, 1 right) 
        max_speed (0 stop, 1 full speed))
        '''
        #trigger_yes = 0
        #while not trigger_yes:  # loop until get correct data
            #try:
              #  trigger_send = ser_ard.readline().decode().strip()
             #   trigger_yes = int(trigger_send)
            #except:
            #    pass
        # confirmation_data = "ACK"
        # ser_ard.write(confirmation_data.encode())

        # wait for arduino to confirm
        # response = ser_ard.read(len(confirmation_data)).decode()
        # if response == confirmation_data:
        data_to_send = "Y{};{};{};{};{}\n".format(str(servo_pos), str(turn_mode), str(PID_left_right), str(max_speed),
                                                 str(wall_follow))
        ser_ard.write(data_to_send.encode())
        print(data_to_send.encode())
        time.sleep(0.1)  # wait for arduino to receive data

        # print(data_to_send)

    # close everything when down
    open_series = 0
    is_closed, ser_ard = connect_ard.ConnArd(open_series, ser_ard)
    if is_closed:
        print("Arduino port is closed")
    else:
        print("Arduino port is not closed")
    cap.release()
