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

# p1 = urc.readWrite("get_actual_tcp_pose()",write,read)

# pose = p1
# direction = "[1,0,0,0,0,0]"
# power = "[-5,5,5,0,0,0]"

# command = "force_mode("+pose+", "+direction+","+power+",2,[0.5,0.5,2,0.5,0.5,0.5])"
# urc.asyncWrite(command,write,read)

print(urc.readWrite("get_actual_joint_positions()",write,read))

urc.closeReadWrite(write,read)