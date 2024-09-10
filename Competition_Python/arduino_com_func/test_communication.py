import serial
import connect_ard

ser_ard = []
open_series = 1
is_open, ser_ard = connect_ard.ConnArd(open_series, ser_ard)
if is_open:
    print("Arduino port {} is open".format(ser_ard.name))
else:
    print("Arduino port is not open")

while True:
    servo_pos = -1
    turn_mode = 1
    PID_left_right = 0.5
    max_speed = 0.3
    wall_follow = 1
    data_to_send = "{};{};{};{};{}\n".format(str(servo_pos), str(turn_mode), str(PID_left_right), str(max_speed),
                                                     str(wall_follow))
    print(data_to_send)
    ser_ard.write(data_to_send.encode())
