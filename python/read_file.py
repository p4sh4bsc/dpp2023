import serial
import struct
import sys
from PIL import Image
import io
import time
import schedule
import os

global stop_it

data = b''
flag = False

ser = serial.Serial("/dev/ttyUSB7", baudrate = 57600)
ser1 = serial.Serial('/dev/ttyACM9', 9800)

ser.setDTR(False)
time.sleep(1)
#command = str(input("aga: "))


check=str
i=0
stop_it=False

flag_r = True



while flag_r:

    if  i > 7 and data[-1] == 100 and data[-2] == 110 and data[-3] == 101 :
        try:
            
            data = data[0:-3]
            
            print(len(data))
            img = Image.open(io.BytesIO(data))

            img.save("/home/rosuser/Downloads/img_from_bytes_for_main.jpg")
            print(len(data))
            data = b''
            i=0
            time.sleep(3)
            break
            flag_r=False
        except:
            print("error")
            i=0
            data = b''
            
            
            
    elif i >= 3 and data[-4::] == b'stop':
        print('stop me')
        try:
            ser1.write(b'LL')
            data = b''
            i=0
        except Exception as ex:
            data = b''
            i=0
            print(ex)
            
            
    elif len(data)>=7000:
        i=0
        data = b''


    else:
        print('while read')

        check = ser.read()
        #print(check)
        data+=check
        print(data, i)
        i+=1
        #print(data)



    
