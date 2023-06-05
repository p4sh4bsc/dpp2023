import serial
import struct
import sys
from PIL import Image
import io
import time

global stop_it

data = b''
flag = False

ser = serial.Serial("/dev/ttyUSB3", baudrate = 57600)
ser1 = serial.Serial('/dev/ttyACM2', 9800)

ser.setDTR(False)
time.sleep(1)
command = str(input("aga: "))


check=str
i=0
stop_it=False

while True:


        check = ser.read()
        data+=check
        print(data)
            #print(data)
        i+=1
            #print(data)
        

    

    #img = Image.frombytes("L", (70, 70), data, decoder_name='raw')
    #img.save('img_frombytes.jpeg')


    

