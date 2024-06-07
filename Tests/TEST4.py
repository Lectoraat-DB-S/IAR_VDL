import URCommunication as urc

IP_UR = "192.168.0.13"
PORT_RECIEVE = 30022

TOOL_IN = 0
TOOL_FLUSH = 13 
TOOL_OUT = 55

TCP = ["p[-0.211457, -0.001123, 0.100158, 0.000000, -1.570796, 0.000000]","p[-0.196577, 0.008553, 0.068163, 0.000000, -1.570796, 0.000000]"]# 0 = Schroeftool TCP; 1 = Sensor TCP.
TCP_SCREWDRIVER = TCP[0]
TCP_SENSOR = TCP[1]

urc.greenLightUR(IP_UR)
write,read = urc.connectReadWrite(IP_UR,PORT_RECIEVE)

pose = "[0,-1.570,1.570,0,1.570,-1.570]"
transpose = "p[0,0,0,0,0,0]"

# Test pose transposing etc.
urc.syncWrite("movel(pose_trans("+transpose+", get_forward_kin("+pose+")))",write,read)

urc.closeReadWrite(write,read)