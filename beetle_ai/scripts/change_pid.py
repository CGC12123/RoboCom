import time
from turtle import goto
from pymycobot.mycobot import MyCobot
import serial.tools.list_ports
# import numpy as np

data_id = [21, 22, 23, 24, 26, 27] 
mc = []
ports = []

def setup():                                                    #机械臂检测函数，选择正确的串口
    global mc
    print("")

    # plist = list(serial.tools.list_ports.comports())
    # idx = 0
    # for port in plist:
    #     print("{} : {}".format(idx, port))
    #     idx += 1
    # if idx == 0:
    #     print("The connected device was not detected. Please try reconnecting.")
    #     exit(1)
    # _in = input("\nPlease input 0 - {} to choice, you can choice many like: '2,1,3':".format(idx))
    # idxes = _in.split(',')
    # try:
    #     idxes = [int(i) for i in idxes]
    # except Exception:
    #     print('Error: Input format error.')
    #     exit(1)

    # ports =  = [str(plist[i]).split(' - ')[0].strip() for i in idxes]
    ports = ["/dev/arm"]
    print(ports)
    print("")

    baud = 115200
    # _baud = input("Please input baud(default:115200，can input 1000000):")
    # try:
    #     baud = int(_baud)
    # except Exception:
    #     pass
    print(baud)
    print("")

    for port in ports:
        try:
            mycobot = MyCobot(port, baud)
            mycobot.power_on()
            mycobot.set_color(0,0,255)#blue, arm is busy  
            mycobot.send_angles([0,0,0,0,0,0],30)
            time.sleep(5)
        except Exception as e:
            print(e)
            exit(1)
        mc.append(mycobot)

def change():
    global mc

    mode = 3
    # _mode = input("Please input mode, 1 = high precision, 2 = stabilize ,3 = testmode1, 4 = testmode2, 5 = testmode3 (default: 1 ):")
    # try:
    #     mode = int(_mode)
    # except Exception:
    #     pass
    print(mode)
    print("")

    for _mycbot in mc:
        print(_mycbot)
        for i in range(1,7):
            if mode == 1:
                data    = [10, 0, 1, 0, 3, 3]
            elif mode == 2:
                if i < 4 :
                    data = [14, 14, 0, 0, 3, 3]
                else:
                    data = [32, 32, 0, 0, 3, 3]
            elif mode == 3:
                data    = [32, 32, 0, 0, 3, 3]
            elif mode == 4:
                data    = [25, 25, 0, 0, 3, 3]
            elif mode == 5:
                data    = [20, 20, 0, 0, 3, 3]
            elif mode == 6:
                data    = [18, 18, 0, 0, 3, 3]
            elif mode == 7:
                data    = [14, 14, 0, 0, 3, 3]
            else:
                print("Please set the parameter mode !!!")
                goto(change())
            
            for j in range(len(data_id)):
                _mycbot.set_servo_data(i, data_id[j], data[j])
                time.sleep(0.2)
                _data = _mycbot.get_servo_data(i, data_id[j])
                time.sleep(0.2)
                if _data == data[j]:
                    print("Servo motor :" + str(i) + "  data_id : " + str(data_id[j]) + "   data: " + str(_data) + "  modify successfully ")
                else:
                    print("Servo motor :"  + str(i) + "  data_id : " + str(data_id[j]) + "   data: " + str(_data) + "  modify error ")
            
    mc[0].set_color(0,255,0)#green, arm is free

if __name__ == "__main__":                                      #主函数
    setup()
    print(mc)
    try:
        change()                            
    except Exception as e:
        print(e)

    


