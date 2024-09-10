from strategy import PID_controller

Kp = 15.0
Ki = 0.1
Kd = 5.00
setpoint_distance = 300# target distance in mm
pid_controller = PID_controller.PIDController(Kp, Ki, Kd, setpoint_distance)


def RightWallFollowing(distance_front, distance_left, distance_right, uturn_threth, exit_threth):
    # # -1 tank turn sig, 0 stop sig, 1 normal turn sig
    # # during turning, -1 left, 0 straight forward,1 right
    # print(distance_front, distance_left, distance_right)
    if distance_left > exit_threth and distance_front > exit_threth and distance_right > exit_threth:  # if distance front and left are too far, left the maze mm
        # stop
        # print('stop')
        return 0, 0
    elif distance_left > uturn_threth and distance_front < exit_threth:  # if the right distance increase suddenly and the front distance is not too far, there is a door   mm
        # fully turn left
        # print('fully turn right')
        return 1, -1
    elif distance_front < 150:  # if too close to front, make tank turn to right mm
        # tank turn left
        # print('tank turn right')
        return -1, 1
    
    

    else:  # wall following
        # print('wall following')
        control = pid_controller.update(distance_left)  # pid control

        # print(control, distance_right)
        control = max(-2000, min(2000, control)) / 2000
    # print(control)
    return 1, control
