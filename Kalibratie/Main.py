import URCommunication as urc
import time
import csv
import math

# Per connection specifics.
IP_UR = "192.168.0.13"
PORT_RECIEVE = 30022

TOOL_IN = 0
TOOL_FLUSH = 13
TOOL_OUT = 55

measuredCounter = 0

# Functions
def MeasurePoint(write_conn,read_conn):
    global measuredCounter
    curPose = urc.readWrite("get_actual_tcp_pose()",write_conn,read_conn)
    print(curPose)
    urc.asyncWrite("measure_point()",write_conn)
    while urc.read(read_conn) == 1:
        print("Waiting...")
    print("Done")
    time.sleep(0.5)
    measuredPoint = urc.readWrite("get_actual_tcp_pose()",write_conn,read_conn)
    print("[COBOT] Position is: " + measuredPoint)
    urc.syncWrite("movel(" + curPose + ",a=1.2,v=0.25,t=0,r=0)",write_conn,read_conn)

    try:
        with open("Kalibratie/Measurements/points.csv", mode="a", newline = '') as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(["Point" + str(measuredCounter),measuredPoint])
            measuredCounter = measuredCounter + 1
    except Exception as err:
        print(err)

def readPoint(filename,index):
    try:
        with open("Kalibratie/Measurements/" + filename, mode="r", newline='') as f:
            reader = csv.reader(f, delimiter=",")
            result = (list(reader)[index])
            return result
    except IndexError:
        print("[ERROR] Index out of range, read failed, return will be wrong.")
    except FileNotFoundError:
        print("[ERROR] File not found! Did you spell the name correctly, and is it in the 'Measurements' folder?")

# Script part.
print(readPoint("points.csv",0))
print(readPoint("points.csv",1))

# urc.greenLightUR(IP_UR)
# write,read = urc.connectReadWrite(IP_UR,PORT_RECIEVE)

# starting_position = "p[-0.359385,0.175107,0.178234,0.00322613,3.14051,0.00389871]"

# #urc.syncWrite("movej(" + starting_position +")",write,read)
# urc.asyncWrite("sd_move(" + str(TOOL_IN) + ",0)",write)
# MeasurePoint(write,read)
# urc.asyncWrite("sd_move(" + str(TOOL_FLUSH) + ",0)",write)
# MeasurePoint(write,read)
# urc.closeReadWrite(write,read)