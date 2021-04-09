
#################################################################################################

## Module based on  Calvin (calvin@inno-maker.com)/ www.inno-maker.com code.

## Author      :dicharisis

## Environment :  Hardware            ----------------------  Raspberry Pi 4
##                Version of Python   ----------------------  Python 3.7.3(Default in the system)

##################################################################################################

import sys
import os
import can
from datetime  import datetime
from time      import time
import json


#Style class definition
class Style:
    def __init__(self):

        #Background console color codes
        self.bg_color = dict()
        self.bg_color['reset']      = '\033[0m'
        self.bg_color['black']      = '\033[40m'
        self.bg_color['red']        = '\033[41m'
        self.bg_color['green']      = '\033[42m'
        self.bg_color['yellow']     = '\033[43m'
        self.bg_color['blue']       = '\033[44m'
        self.bg_color['purple']     = '\033[45m'
        self.bg_color['light_blue'] = '\033[46m'
        self.bg_color['white']      = '\033[47m'

        #Text console color code
        self.txt_color = dict()
        self.txt_color['white']      = '\033[37m'
        self.txt_color['light_blue'] = '\033[36m'
        self.txt_color['purple']     = '\033[35m'
        self.txt_color['blue']       = '\033[34m'
        self.txt_color['yellow']     = '\033[33m'
        self.txt_color['green']      = '\033[32m'
        self.txt_color['red']        = '\033[31m'
        self.txt_color['black']      = '\033[30m'
        self.txt_color['reset']      = '\033[0m'

 
#Message Class definition
class Message(Style):
    config = dict()

    def __init__(self,msg):
        super().__init__() 
        self.msg = msg
        self.counter = 0
        self.msg_info =" " 
        self.info = " "
        self.time_stamp = 0
        self.msg_recv_time=0
        self.msg_recv_time_previous=0

    #Counts cycle of receiving in ms 
    def cycle_timer(self):
        if self.msg_recv_time_previous ==0 :
            self.msg_recv_time_previous = self.msg.timestamp


        else:
            self.msg_recv_time =self.msg.timestamp - self.msg_recv_time_previous
            self.msg_recv_time_previous = self.msg.timestamp

    def incr(self):
        if self.counter == 10000 :
            self.counter = 0
        else:
            self.counter +=1


    def get_timestamp(self):
       self.time_stamp = datetime.fromtimestamp(self.msg.timestamp)
       return   self.time_stamp


    def dynamic_Print(self):
        print("\n ")
        
        print('\033[K'  + self.txt_color['red']+ 'ID =  '+str(hex( self.msg.arbitration_id))            +self.bg_color['black']+'  '+
              '\033[K'  + self.txt_color['blue']+ 'DLC = '+str(self.msg.dlc)                            +self.bg_color['black']+'  '+
              '\033[K'  + self.txt_color['blue']+ 'Descr = '+self.msg_info                              +self.bg_color['black']+'  '+
              '\033[K'  + self.txt_color['green']+ 'Counts = '+str(self.counter)                        +self.bg_color['black']+'  '+
              '\033[K'  + self.txt_color['purple']+ 'TimeStamp = '+str(self.time_stamp)                 +self.bg_color['black']+'  '+
              '\033[K'  + self.txt_color['light_blue']+'Cycle = '+str( int ((self.msg_recv_time)*1000) )+' ms')
        
    @classmethod
    def config_apply(cls,file,mode):

        try:
            with open(file,mode) as settings_file:

                cls.config = json.load(settings_file)
        except:
            print("Error handling confguration file inside Message Class ")




    def __repr__(self):
        self.info = 'This is an instance of Message Class that inherits Style Class'
        return self.info



#CAN Class Definition
class CAN:

    def __init__(self, name= 'can0' , bitrate= '125000'):
        os.system('sudo ip link set ' + name + ' type can bitrate ' + bitrate)
        os.system('sudo ifconfig ' + name + ' up')
        self.bus = can.interface.Bus(channel = name, bustype = 'socketcan_ctypes')
        




#Main function sniffing and printing CanBus messages
def Serve_Can():

    os.system('clear')

    canbus = CAN('can0','125000').bus

    buffer = { }
    style =  Style()

    Message.config_apply('config_data.json','r')


    try:
        while True:

            #moves cursor in position X:0 ,Y:0
            os.system(" printf '\033[0;0H] ' ")

            #Receives Can bus messages (blocking function )
            msg = canbus.recv(30.0)


            #30seconds passed without a message
            if msg is None:
                print('No message was received')
        
            #Message recieved and exists inside our buffer
            elif msg.arbitration_id in buffer:

                buffer[msg.arbitration_id].msg = msg
    
                buffer[msg.arbitration_id].incr()

                buffer[msg.arbitration_id].get_timestamp()

                buffer[msg.arbitration_id].cycle_timer()

                id = str(hex(msg.arbitration_id ))
                #check if message is in defined in our config file
                if id in Message.config['messages']:
                    buffer[msg.arbitration_id].msg_info = Message.config['messages'][id]

            #New message received create new Message class
            else:
                buffer[msg.arbitration_id] = Message(msg)

            #Print content   
            for message in buffer:
                buffer[message].dynamic_Print()
    except:
        os.system('clear')
        print("Error in main loop or signal for stop   ")
        os.system('sudo ifconfig can0 down')


#Main function 

Serve_Can()
