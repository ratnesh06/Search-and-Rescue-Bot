import serial
import serial.tools.list_ports as SerialPortList

def ConnArd(turn_onoff, ser):
    '''

    :param turn_onoff: 1 - turn on. 0 - turn off
    :return: 1- open or close, 0 - fail
    '''
    if turn_onoff:
        lidar_baudrate = 9600
        usb_type = str('Arduino')
        usb_type_2 = str('modem')
        usb_type_3 = str('ACM')
        usb_count = 0
        for port_name in SerialPortList.comports():
            print(port_name)
            if usb_type in str(port_name):
                break
            elif usb_type_2 in str(port_name):
                break
            elif usb_type_3 in str(port_name):
                break
            else:
                usb_count += 1

        serial_name = str(list(SerialPortList.comports())[usb_count][0])
        ser = serial.Serial(serial_name, lidar_baudrate)  # open usb port,set baudrate
        if ser.isOpen():  # if the serial is open
            return 1, ser
        else:
            return 0, []

    if not turn_onoff:
        ser.close()  # close usb port
        if not ser.isOpen():  # if the serial is closed
            return 1, []
        else:
            return 0, []
