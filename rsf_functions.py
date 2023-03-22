import configparser
import os

def check_file_exists(file):
    return os.path.isfile(file)

class CFG_RBR:
    ScreenX = 0
    ScreenY = 0
    dash_file = ""
    
    def get_dash_file_by_res(self, xRes, yRes):
        aspect=xRes / yRes
        if aspect > 4/3:
            aspect=4/3
        reso43AspectRatio=(aspect * yRes)
        if(reso43AspectRatio < 800):
            return "DIGIDASH_640.ini"
        elif(reso43AspectRatio < 1024):
            return "DIGIDASH_800.ini"
        elif(reso43AspectRatio < 1280):
            return "DIGIDASH_1024.ini"
        elif(reso43AspectRatio < 1600):
            return "DIGIDASH_1280.ini"
        else:
            return "DIGIDASH.ini"
    
    def __init__(self, rbr_dir):
        config = configparser.ConfigParser()
        if (check_file_exists(rbr_dir  + "RichardBurnsRally.ini") == False):
            print("Config file not found")
            exit(1)
        config.read(rbr_dir  + "RichardBurnsRally.ini")
        self.ScreenX = config.getint('Settings', 'XRes')
        self.ScreenY = config.getint('Settings', 'YRes')
        print("Y res:" + str(self.ScreenY))
        print("X res:" + str(self.ScreenX))
        
        self.dash_file = rbr_dir + "misc\\" + self.get_dash_file_by_res(self.ScreenX, self.ScreenY)
        if (check_file_exists(self.dash_file) == False):
            print("dash file not found")
            exit(1)
            
        print("Dash file:" + self.dash_file)

