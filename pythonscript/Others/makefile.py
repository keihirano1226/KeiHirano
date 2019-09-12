import os
import sys

basepass = sys.argv[1]
os.mkdir(basepass + "depth_mirror")
os.mkdir(basepass + "color_mirror")
os.mkdir(basepass + "color")
os.mkdir(basepass + "regi")
os.mkdir(basepass + "regi_mirror")
