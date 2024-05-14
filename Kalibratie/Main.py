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

starting_position = "p[-0.523536,0.0793283,-0.033546,-1.03541,-1.50049,-1.48552]"

urc.syncWrite("movej(" + starting_position +")",write,read)
# urc.asyncWrite("sd_move(" + str(TOOL_IN) + ",0)",write)
# print("1st Measurement: " + str(st.MeasurePoint(write,read)))
# urc.asyncWrite("sd_move(" + str(TOOL_FLUSH) + ",0)",write)
# # Moving pos
# urc.syncWrite("movel(p[-0.555281,0.079289,-0.0335189,-1.03533,-1.50048,-1.48548])",write,read)
# print("2nd Measurement: " + str(st.MeasurePoint(write,read)))

st.MeasureEdge(write,read)

urc.closeReadWrite(write,read)