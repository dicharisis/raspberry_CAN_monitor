
#################################################################################################

## Module based on  Calvin (calvin@inno-maker.com)/ www.inno-maker.com code.

## Author      :dicharisis

## Environment :  Hardware            ----------------------  Raspberry Pi 4
##                Version of Python   ----------------------  Python 3.7.3(Default in the system)

##################################################################################################

import sys

import os
import can

from message  import Message
from my_can   import CAN
from style    import Style

#Main function sniffing and printing CanBus messages
def Serve_Can():

    os.system('clear')
    
    Message.config_apply('config_data.json','r')
  
    channel = 'can0'
    bitrate = '125000'
    canbus = CAN(channel,bitrate).bus

    buffer = {}
    style =  Style()



    try:
        while True:

            #moves cursor in position X:0 ,Y:0M
            os.system(" printf '\033[0;0H] ' ")
            print("\033[31m CHANNEL --> {}  Bitrate --> {} bit/sec ".format(channel,bitrate ) )
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

                buffer[msg.arbitration_id].data_handle(id)
                #check if message is defined in our config file
                #if id in Message.config['messages']:
                   # buffer[msg.arbitration_id].msg_info = Message.config['messages'][id]

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

if __name__ == '__main__':
    Serve_Can()
