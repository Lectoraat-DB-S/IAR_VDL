import URCommunication as urc
import time

# Per connection specifics.
IP_UR = "192.168.0.13"
PORT_RECIEVE = 30022

TOOL_IN = 0
TOOL_FLUSH = 13
TOOL_OUT = 55

urc.greenLightUR(IP_UR)
write,read = urc.connectReadWrite(IP_UR,PORT_RECIEVE)

print(urc.readWrite("get_actual_tcp_pose()",write,read))

urc.closeReadWrite(write,read)