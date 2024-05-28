import URCommunication as urc
import Storage as st
import time
import math

# Per connection specifics.
IP_UR = "192.168.0.13"
PORT_RECIEVE = 30022

TOOL_IN = 0
TOOL_FLUSH = 13
TOOL_OUT = 55

# Functions
# Script part.
print(st.readPoint("points.csv",0))
print(st.readPoint("points.csv",1))

urc.greenLightUR(IP_UR)
write,read = urc.connectReadWrite(IP_UR,PORT_RECIEVE)

# Main body.

# First, we need to calculate the position of our object by measuring 3 pre-defined points.
# Make path to measure the needed points.

# Then running the mathematics code (for a example, look in "TEST2.py").

# Angle of rotation is rZ on base.
# See RoboDK area for standard positions.

urc.closeReadWrite(write,read)