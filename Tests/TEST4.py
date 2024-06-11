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

Centre_Point = "p(-1.011832, 0.047732, -0.0871,0.0,0.0,0.0)"
Point1 = "p(-0.098,0.1155,0.0755,-0.034,1.571,-0.034)"
base = "p(0.0,0.0,0.0,0.0,0.0,0.0)"


# Test pose transposing etc.
urc.syncWrite("movel(pose_trans("+Centre_Point+", "+Point1+"))",write,read)

urc.closeReadWrite(write,read)