from mover import Mover
import struct
import serial
import time


class Coder:
    def code(self, a, b):
        return struct.pack('>ch', bytes(a, encoding='utf-8'), int(b))

    def decode(self, command):
        return struct.unpack('>ch', command)

class Worker:
    def __init__(self):
        self.mover = Mover()

    def run(self, command):
        com = command[0:1]
        number = command[1::]
        number = float(number)
        print(com)
        print(number)
        print(type(number))
        if com == 'A':
            self.mover.led(number)
        if com == 'B':
            self.mover.forward(number)

        



if __name__ == '__main__':
    cd = Coder()
    worker = Worker()
    command = str(input("vvedi: "))
    worker.run(command)

