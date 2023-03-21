from GUI import Init_GUI
from dash import RBR_DASH
from debug import dbg
#from rsf_functions import CFG_RBR

def main():
    dash = RBR_DASH()
    Init_GUI(dash)
    dbg("JOB DONE")

if __name__ == "__main__":
    main()
