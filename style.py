#Style class 
#A class that helps adding color style  in terminal

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


