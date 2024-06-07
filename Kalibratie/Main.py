import URCommunication as urc
import Storage as st
import Calibration as cal
import time
import math

# Per connection specifics.
IP_UR = "192.168.0.13"
PORT_RECIEVE = 30022

TOOL_IN = 0
TOOL_FLUSH = 13 
TOOL_OUT = 55

TCP = ["p[-0.211457, -0.001123, 0.100158, 0.000000, -1.570796, 0.000000]","p[-0.196577, 0.008553, 0.068163, 0.000000, -1.570796, 0.000000]"]# 0 = Schroeftool TCP; 1 = Sensor TCP.
TCP_SCREWDRIVER = TCP[0]
TCP_SENSOR = TCP[1]

MeasurementPoses = [
    ["[-0.690796,-1.46479,2.05802,-0.585906,-0.702562,0.0167929]","[-0.755371,-1.43441,2.02297,-0.581487,-0.767256,0.0174955]"], #Back side.
    ["[-0.70979,-0.491054,1.31468,2.25931,-0.844268,0.0379639]","[-0.680549,-0.44912,1.21117,2.32224,-0.873493,0.0359359]"], # Left side.
    ["placeholder_1","placeholder_2"], # Front side.
    ["placeholder_3","placeholder_4"] # Right side.
    ]
InbetweenPoses = [
    "[-1.0023,-1.04478,1.54754,-0.448062,-0.0243877,1.52694]", # Back to left.
    "placeholder_5", # Left to front.
    "placeholder_6", # Front to right.
    "placeholder_7", # Right to back.
    ]

# This is the value used to calculate the final offset.
# Change this into a variable read from generated URScript, instructions for this should be inside other documentation.
DigitalMiddlePoint = urc.poseToValues("p[-1.011832,0.047732,-0.0871,0.0,0.0,0.0]")


def DoCalibration(write_conn,read_conn):
    urc.syncWrite("movel("+InbetweenPoses[0]+")",write_conn,read_conn)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write_conn,read_conn)

    urc.syncWrite("movel("+MeasurementPoses[0][0]+")",write_conn,read_conn)
    urc.syncWrite("set_tcp("+ TCP_SENSOR +")",write_conn,read_conn)
    measurement_0_0 = st.MeasurePoint(write_conn,read_conn,0)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write_conn,read_conn)


    # Take measurement 2: High-Back 2.
    urc.syncWrite("movej("+MeasurementPoses[0][1]+")",write_conn,read_conn)
    urc.syncWrite("set_tcp("+ TCP_SENSOR +")",write_conn,read_conn)
    measurement_0_1 = st.MeasurePoint(write_conn,read_conn,1)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write_conn,read_conn)

    # Move through inbetween position.
    urc.syncWrite("movel("+InbetweenPoses[0]+")",write_conn,read_conn)

    # Take measurement 3: Low-Left.
    urc.syncWrite("movel("+MeasurementPoses[1][0]+")",write_conn,read_conn)
    urc.syncWrite("set_tcp("+ TCP_SENSOR +")",write_conn,read_conn)
    measurement_1_0 = st.MeasurePoint(write_conn,read_conn,2)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write_conn,read_conn) 

    urc.syncWrite("movel("+MeasurementPoses[1][1]+")",write_conn,read_conn)
    urc.syncWrite("set_tcp("+ TCP_SENSOR +")",write_conn,read_conn)
    measurement_1_1 = st.MeasurePoint(write_conn,read_conn,3)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write_conn,read_conn)

    # WIP: Add 2 measurement positions for the front here.

    # WIP: Add 2 measurement positions for the right here.

    # Returning back to inbetween position.
    urc.syncWrite("movel("+InbetweenPoses[0]+")",write_conn,read_conn)

    # print("------- Outputs -------")
    # print(urc.poseToValues(measurement_1))
    # print(urc.poseToValues(measurement_2))
    # print(urc.poseToValues(measurement_3))
    # print("-----------------------")

    measurements = [[measurement_0_0,measurement_0_1],[measurement_1_0,measurement_1_1]]

    measurement_1 = urc.poseToValues(measurement_1)
    measurement_2 = urc.poseToValues(measurement_2)
    measurement_3 = urc.poseToValues(measurement_3)
    measurement_4 = urc.poseToValues(measurement_4)

    a = [float(measurements[0][0][0]),float(measurement_1[0][0][1]),float(measurement_1[0][0][5])]
    b = [float(measurements[0][1][0]),float(measurements[0][1][1]),float(measurements[0][1][5])]
    c = [float(measurements[1][0][0]),float(measurements[1][0][1]),float(measurements[1][0][5])]
    d = [float(measurements[1][1][0]),float(measurements[1][1][1]),float(measurements[1][1][5])]
    e = [float(measurements[2][0][0]),float(measurements[2][0][1]),float(measurements[2][0][5])]
    f = [float(measurements[2][1][0]),float(measurements[2][1][1]),float(measurements[2][1][5])]
    g = [float(measurements[3][0][0]),float(measurements[3][0][1]),float(measurements[3][0][5])]
    h = [float(measurements[3][1][0]),float(measurements[3][1][1]),float(measurements[3][1][5])]
    out = cal.CalculateOffsets([a,b,c,d,e,f,g,h],DigitalMiddlePoint)
    # print("Debug: " + str(out[0]) + ", " + str(out[1]) + ", " + str(math.degrees(out[2])))
    return [out[0],out[1],out[2]]

# Start of runtime code.

urc.greenLightUR(IP_UR)
write,read = urc.connectReadWrite(IP_UR,PORT_RECIEVE)

r=[[],[],[],[],[],[],[]]

# Main body.
r[0] = DoCalibration(write,read)
r[1] = DoCalibration(write,read)
r[2] = DoCalibration(write,read)
r[3] = DoCalibration(write,read)
r[4] = DoCalibration(write,read)
r[5] = DoCalibration(write,read)
r[6] = DoCalibration(write,read)
print("[DEBUG] Offset values: "+ str(r[0]))
print("[DEBUG] Offset values: "+ str(r[1]))
print("[DEBUG] Offset values: "+ str(r[2]))
print("[DEBUG] Offset values: "+ str(r[3]))
print("[DEBUG] Offset values: "+ str(r[4]))
print("[DEBUG] Offset values: "+ str(r[5]))
print("[DEBUG] Offset values: "+ str(r[6]))

urc.closeReadWrite(write,read)

# # Debugging input thing
# measurement_1 = [-0.571832, -0.0329811, 0.336053, 1.18806, 1.23434, 1.16952]
# measurement_2 = [-0.571194, -0.00485261, 0.333504, 1.18808, 1.23436, 1.16951]
# measurement_3 = [-1.05558, 0.438235, 0.202389, -1.53864, -0.10022, -0.0133398]

