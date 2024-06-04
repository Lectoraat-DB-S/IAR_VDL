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

MeasurementPoses = ["[-0.690796,-1.46479,2.05802,-0.585906,-0.702562,0.0167929]","[-0.755371,-1.43441,2.02297,-0.581487,-0.767256,0.0174955]","[-0.700706,-0.759412,1.32686,-0.6222,0.853325,3.17627]"]
InbetweenPoses = ["[-1.0023,-1.04478,1.54754,-0.448062,-0.0243877,1.52694]"]
DigitalMiddlePoint = urc.poseToValues("p[-1.011832,0.047732,-0.0871,0.0,0.0,0.0]")
print(DigitalMiddlePoint)

urc.greenLightUR(IP_UR)
write,read = urc.connectReadWrite(IP_UR,PORT_RECIEVE)

# Main body.

# First, we need to calculate the position of our object by measuring 3 pre-defined points.
# Make path to measure the needed points.

# Then running the mathematics code (for a example, look in "TEST2.py").

# Angle of rotation is rZ on base.
# See RoboDK area for standard positions.


# Some measured positions in Poses:
# Measurement Pose High-Back 1: p[-0.456794,-0.00533451,0.332255,1.18821,1.23445,1.16951]
# Measurement Pose High-Back 2: p[-0.456794,-0.0334881,0.334757,1.18805,1.23438,1.16955]
# Measurement Pose Low-Left:  p[-1.06327,0.573519,0.206323,-1.53862,-0.100178,-0.0132888]
# urc.syncWrite("movel("+InbetweenPoses[0]+")",write,read)

# Take measurement 1: High-Back 1.

# For stability.
def DoCalibration():
    urc.syncWrite("movel("+InbetweenPoses[0]+")",write,read)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write,read)

    urc.syncWrite("movel("+MeasurementPoses[0]+")",write,read)
    urc.syncWrite("set_tcp("+ TCP_SENSOR +")",write,read)
    measurement_1 = st.MeasurePoint(write,read,0)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write,read)


    # Take measurement 2: High-Back 2.
    urc.syncWrite("movej("+MeasurementPoses[1]+")",write,read)
    urc.syncWrite("set_tcp("+ TCP_SENSOR +")",write,read)
    measurement_2 = st.MeasurePoint(write,read,1)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write,read)

    # Move through inbetween position.
    urc.syncWrite("movel("+InbetweenPoses[0]+")",write,read)

    # Take measurement 3: Low-Left.
    urc.syncWrite("movel("+MeasurementPoses[2]+")",write,read)
    urc.syncWrite("set_tcp("+ TCP_SENSOR +")",write,read)
    measurement_3 = st.MeasurePoint(write,read,2)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write,read) 

    urc.syncWrite("movel("+MeasurementPoses[3]+")",write,read)
    urc.syncWrite("set_tcp("+ TCP_SENSOR +")",write,read)
    measurement_3 = st.MeasurePoint(write,read,3)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write,read)

    # Returning back to inbetween position.
    urc.syncWrite("movel("+InbetweenPoses[0]+")",write,read)

    # print("------- Outputs -------")
    # print(urc.poseToValues(measurement_1))
    # print(urc.poseToValues(measurement_2))
    # print(urc.poseToValues(measurement_3))
    # print("-----------------------")

    measurement_1 = urc.poseToValues(measurement_1)
    measurement_2 = urc.poseToValues(measurement_2)
    measurement_3 = urc.poseToValues(measurement_3)
    measurement_4 = urc.poseToValues(measurement_4)

    a = [float(measurement_1[0]),float(measurement_1[1]),float(measurement_1[5])]
    b = [float(measurement_2[0]),float(measurement_2[1]),float(measurement_2[5])]
    c = [float(measurement_3[0]),float(measurement_3[1]),float(measurement_3[5])]
    d = [float(measurement_4[0]),float(measurement_4[1]),float(measurement_4[5])]
    out = cal.CalculateOffsets([a,b,c],DigitalMiddlePoint)
    # print("Debug: " + str(out[0]) + ", " + str(out[1]) + ", " + str(math.degrees(out[2])))
    return [out[0]-0.0039,out[1]-0.019,out[2]]

print("[DEBUG] Offset values: "+ str(DoCalibration()))
print("[DEBUG] Offset values: "+ str(DoCalibration()))
print("[DEBUG] Offset values: "+ str(DoCalibration()))
print("[DEBUG] Offset values: "+ str(DoCalibration()))
print("[DEBUG] Offset values: "+ str(DoCalibration()))

urc.closeReadWrite(write,read)

# # Debugging input thing
# measurement_1 = [-0.571832, -0.0329811, 0.336053, 1.18806, 1.23434, 1.16952]
# measurement_2 = [-0.571194, -0.00485261, 0.333504, 1.18808, 1.23436, 1.16951]
# measurement_3 = [-1.05558, 0.438235, 0.202389, -1.53864, -0.10022, -0.0133398]

