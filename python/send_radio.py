import struct
import serial
import time


class Coder:
    def code(self, command):
        com, number = command.split()
        return struct.pack('>ch', bytes(com, encoding='utf-8'), int(number))

    def decode(self, command):
        return struct.unpack('>ch', command)




if __name__ == '__main__':
    cd = Coder()
    print(1)
    values = bytearray([4, 9, 62, 144, 56, 30, 147, 3, 210, 89, 111, 78, 184, 151, 17, 129])
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    ser.setDTR(False)
    
    while True:
        ser.write(values)
        time.sleep(1)
