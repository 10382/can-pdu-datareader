# -*- coding: utf-8 -*-

import serial
import time
import struct
import pandas as pd

# 有功电能清空函数
def clear_consum(ser):
    h_consum_clr = b'\x01\x06\x00\x04\xaa\xbb\xf6\xd8'
    l_consum_clr = b'\x01\x06\x00\x05\xaa\xbb\xa7\x18'
    ser.write(h_consum_clr)
    flag = 0
    if ser.readline() == h_consum_clr:
        flag = 1
    ser.write(l_consum_clr)
    if flag == 1 and ser.readline() == l_consum_clr:
        print("用电量清零成功！")
    else:
        print("用电量清空失败！！！")

def get_data(ser, filename):
    data_rec = b'\x00\x00'
    while len(data_rec) != 17 or data_rec[0:2] != b'\x01\x03':
        time_send = int(time.time())
        # print(time.mktime(time.localtime()))
        ser.write(b"\x01\x03\x00\x00\x00\x06\xc5\xc8")
        # data_rec = ser.read(17)
        data_rec = ser.readline()
        # time_rec = time.time()
        print(time_send)
        while len(data_rec) < 17:
            data_break = ser.readline()
            if data_break == b'':
                print("break!")
                break
            elif data_rec[-1:] == b'\n':
                data_rec = data_rec + data_break
        # print(data_rec)

    voltage = struct.unpack('!I', b'\x00\x00' + data_rec[3:5])[0] / 10.0
    current = struct.unpack('!I', b'\x00\x00' + data_rec[5:7])[0] / 100.0
    power = struct.unpack('!I', b'\x00\x00' + data_rec[7:9])[0]
    power_factor = struct.unpack('!I', b'\x00\x00' + data_rec[9:11])[0] / 1000.0
    power_consum = struct.unpack('!L', data_rec[11:15])[0]
    df = pd.DataFrame({ 'epoch' : time_send,
                        'voltage' : voltage,
                        'current' : current,
                        'power' : power,
                        'power_factor' : power_factor,
                        'power_consumption' : power_consum }, index=[0])
    df.to_csv(filename, mode='a', header=False, index=False)

    # print("电压:", voltage, "V")
    # print("电流:", current, "A")
    # print("功率:", power, "kW")
    # print("功率因子:", power_factor)
    # print("有功电能:", power_consum, "kWh")
