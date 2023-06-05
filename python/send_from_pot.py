import struct
import serial
import time
import os

class Coder:
    def code(self, command):
        com, number = command.split()
        return struct.pack('>ch', bytes(com, encoding='utf-8'), int(number))

    def decode(self, command):
        return struct.unpack('>ch', command)




if __name__ == '__main__':
    cd = Coder()
    
    check_for_start = True
    
    
    ser1 = serial.Serial('/dev/ttyACM9', 9800)

    
    ser = serial.Serial('/dev/ttyUSB7', 57600)
    ser.setDTR(False)

    flag_exist = False
    check_for_start = False
    file_path = '/home/rosuser/Downloads/img_from_bytes_for_main.jpg'
    while True:
        
            
        
        

        while not check_for_start:
            data_from_radio = ser.read(5)
            #print(data_from_radio)
            if data_from_radio == b'start':
                check_for_start = True
                ser1.write(b'H')
                    
        if os.path.exists(file_path):
            flag_exist=True

        while flag_exist:


            command = b'BGN'
            values = ser1.readline().strip()
            print(values)
            command += values
            command += b'END'
            print(command)
            ser.write(command)
#            time.sleep(6)
            


