from strategy import PID_controller
'''
>390 very close, open door, very slow
>300 close, slow down
'''
Kp = 10.0
Ki = 0.5
Kd = 5.00
setpoint_distance = 500 // 2  # target distance pixel
pid_controller = PID_controller.PIDController(Kp, Ki, Kd, setpoint_distance)


def TrackBall(ball_location):
    '''
    :param ball_location: x,y
    :return: PID_output (how much left or right)
    '''
    ball_x = ball_location[0]
    PID_output = pid_controller.update(ball_x)
    # limit to [-1,1]
    PID_output = max(-2000, min(2000, PID_output)) / 2000
    return PID_output


def SpeedCloseBallandPick(ball_location):
    '''
    :param ball_dis_center: in mm
    :param ball_location: x,y
    :return: percent_speed, servo_pos to arduino
    '''
    if ball_location[1] > 350:  # pix
        percent_speed = 0.3
        servo_pos = 1 # close to ball and open door
    elif ball_location[1] > 300:
        percent_speed = 0.5
        servo_pos = 0
    else:
        percent_speed = 1
        servo_pos = 0
    return percent_speed, servo_pos
