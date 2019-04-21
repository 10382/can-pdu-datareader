# -*- coding: utf-8 -*-

import serial
import time

import monitorfun as mf

interval = 1
time_diff = 0

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)

# for i in range(1):
while True:
    str_filename = time.strftime("/home/njupt/Data/PDU/pdu-%Y-%m-%d.csv", time.localtime())
    # print(str_filename)
    time_remain = interval - (time.time() - time_diff) % interval
    time.sleep(time_remain)
    # 获取当前秒的数据
    mf.get_data(ser, str_filename)
    # # 调用清空有功电能函数
    # mf.clear_consum(ser)

ser.close()
