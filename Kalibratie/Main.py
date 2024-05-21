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

# urc.asyncWrite("sd_move(" + str(TOOL_IN) + ",0)",write)
# print("1st Measurement: " + str(st.MeasurePoint(write,read)))
# urc.asyncWrite("sd_move(" + str(TOOL_FLUSH) + ",0)",write)
# # Moving pos
# urc.syncWrite("movel(p[-0.555281,0.079289,-0.0335189,-1.03533,-1.50048,-1.48548])",write,read)
# print("2nd Measurement: " + str(st.MeasurePoint(write,read)))

urc.syncWrite("movej(p[-0.607434,0.195486,0.0056413,-1.57312,0,0])",write,read)
urc.syncWrite("movel(p[-0.461485,-0.0782624,0.589034,1.17087,-1.25927,-1.17878])",write,read)
urc.syncWrite("movel(p[-0.326471,0.593071,0.361787,1.17087,-1.25927,-1.17878])",write,read)
urc.syncWrite("movel(p[-0.461485,-0.0782624,0.589034,1.17087,-1.25927,-1.17878])",write,read)
urc.syncWrite("movel(p[-0.607434,0.195486,0.0056413,-1.57312,0,0])",write,read)

#WIP Storage
Direct_Offsets = [0.0,0.0]
# Offset X and Y determine rotation through distance.
# More measurements might be needed if there are more than 1 solution.
# Object is 190x190mm.

# I.E : Measurement 1 is 10 cm, 2 is 10cm when both are 90* from eachother, with a magnitude between measurements of ~~ 275.77 mm.
# Measurements above determine a rotation of 0, offset of [0,0]

# Measurement 1 is 9 cm, 2 is 10cm : Offset of [-1,0], rotation 0.
# Is it possible to reach these measurements by any combination of rotation with or without offsets.

# 2 measurements can be taken on 1 face to determine it's angle.
# Which would solve rotation, but lowers it's maximum rotation and/or translation before failure.

# Delta can be calculated from those two measurements, delta to rotation needs 0 position, which can be hardcoded (I.E, Front of table being 0, etc.)
# All values besides X,Y,rX are static.
# Angle Alp. in triangle ABC can be found through stand. A^2 + B^2 = C^2.
# Lenghts taken from Measurement magnitude.

st.MeasurePoint(write,read,0)
# Drop 2 Values depending on measurement. (X,Y,Z)
# Drop rotation values.
# Store value as variable.
#

urc.closeReadWrite(write,read)