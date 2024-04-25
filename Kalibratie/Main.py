import URCommunication as urc
import time

# Per connection specifics.
IP_UR = "192.168.0.13"
PORT_RECIEVE = 30022


# Functions
def MeasurePoint(write_conn,read_conn):
    curPose = urc.readWrite("get_actual_tcp_pose()",write_conn,read_conn)
    print(curPose)
    urc.asyncWrite("measure_point()",write_conn)
    while urc.read(read_conn) == 1:
        print("Waiting...")
    print("Done")
    time.sleep(0.5)
    print("[COBOT] Position is: " + urc.readWrite("get_actual_tcp_pose()",write_conn,read_conn))
    urc.syncWrite("movel(" + curPose + ",a=1.2,v=0.25,t=0,r=0)",write_conn,read_conn)

# Script part.
urc.greenLightUR(IP_UR)
write,read = urc.connectReadWrite(IP_UR,PORT_RECIEVE)

starting_position = "p[-0.359385,0.175107,0.178234,0.00322613,3.14051,0.00389871]"

urc.syncWrite("movej(" + starting_position +")",write,read)
MeasurePoint(write,read)

urc.closeReadWrite(write,read)