import os
import can


#CAN Class Definition
class CAN:

    def __init__(self, name= 'can0' , bitrate= '125000'):
        os.system('sudo ip link set ' + name + ' type can bitrate ' + bitrate)
        os.system('sudo ifconfig ' + name + ' up')
        self.bus = can.interface.Bus(channel = name, bustype = 'socketcan_ctypes')
        

