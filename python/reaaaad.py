import struct
import serial
import time


class Coder:
    def code(self, command):
        com, number = command.split()
        return struct.pack('>ch', bytes(com, encoding='utf-8'), int(number))

    def decode(self, command):
        return struct.unpack('>ch', command)


COMMANDS = ['A', 'B', 'C']

if __name__ == '__main__':
    coder = Coder()
    ser = serial.Serial('/dev/ttyUSB13', 19200)
    ser.setDTR(False)
    while True:
        a = str(input())
        ser.write(coder.code(a))
        if a[0] == 'H':
            im = []
            while True:
                a = time.time()
                s = ser.read()
                b = time.time()
                if bool(s) and b - a < 3:
                    im.append(s)
                else:
                    with open('lol.jpg', 'wb') as file:
                        file.write(b''.join(im))
                    print('Picture accepted')
                    break
        elif a[0] == 'I':
            s = ser.read(4)
            print(s)
        elif a[0] == 'F':
            s = ser.read(1)
            print(s)

