
import struct
import serial
import time


class Coder:
    def code(self, a):
        #return struct.pack('>ch', bytes(a, encoding='utf-8'), int(b))
        return struct.pack('>ch', bytes(a, encoding='utf-8'))
    def decode(self, command):
        return struct.unpack('>ch', command)




if __name__ == '__main__':
    cd = Coder()
    ser = serial.Serial("/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0012-if00-port0", baudrate = 19200)
    #ser = serial.Serial("/dev/ttyUSB0", baudrate = 19200)
    
    s = cd.code('file.txt')
    print(s)
    ser.write(s)
    ser.write(b'end')

