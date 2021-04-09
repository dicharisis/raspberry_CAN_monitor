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


