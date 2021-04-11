from style    import Style
from datetime import datetime
from time     import time
import json

#Message Class definition

class Message(Style):
    config = dict()
    config_applied = False

    def __init__(self,msg):
        super().__init__()

        self.msg = msg

        self.counter = 0

        self.data_handled = {}

        self.info = "Message Class "

        self.time_stamp = 0

        self.msg_recv_time=0

        self.msg_recv_time_previous=0

        self.enable = True
        id = str(hex(msg.arbitration_id))

        if self.__class__.config_applied :
            self.enable = True  if (self.__class__.config["messages"][id]["Enable"] == "ON") else False

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
        if self.enable:
            print("\n ")

            print('\033[K'  + self.txt_color['red']+ 'ID =  '+str(hex( self.msg.arbitration_id))            +" "+
                  '\033[K'  + self.txt_color['blue']+ 'DLC = '+str(self.msg.dlc)                            +" "+
                  '\033[K'  + self.txt_color['green']+ 'Counts = '+str(self.counter)                        +" "+
                  '\033[K'  + self.txt_color['purple']+ 'TimeStamp = '+str(self.time_stamp)                 +" "+
                  '\033[K'  + self.txt_color['light_blue']+'Cycle = '+str( int ((self.msg_recv_time)*1000) )+' ms')

            print('\033[K'  + self.txt_color['green']      +'Data = {}'.format(self.data_handled )          +" "  )


    def data_handle(self,id):
        self.data_handled = {}

        if (self.__class__.config_applied) :

            size_pattern = self.__class__.config["messages"][id]["bytes_per_value"]

            descr_pattern =  self.__class__.config["messages"][id]["data_descr"]


            if (self.msg.dlc == sum(size_pattern) ):

                if self.enable:

                    index=0
                    counter=0
                    for i in size_pattern:

                        value=0
                        for j in range(index,(i+index),1):

                            value = ( (value << 8 ) | self.msg.data[j] )


                        self.data_handled[ descr_pattern[counter] ]= value
                        counter+= 1 
                        index = index + i

            else:
                self.data_handled = [i for i in self.msg.data ] 
                self.data_handled.append("Wrong configuration Data to native form ")



    @classmethod
    def config_apply(cls,file,mode):

        try:

            with open(file,mode) as settings_file:

                cls.config = json.load(settings_file)
                cls.config_applied = True
                
        except:
            print("Error handling confguration file inside Message Class ")
            print("*** NO CONFIG APPLIED ***")



    def __repr__(self):
        self.info = 'This is an instance of Message Class that inherits Style Class'
        return self.info


