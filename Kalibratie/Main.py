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

MeasurementPoses = ["[-0.690796,-1.46479,2.05802,-0.585906,-0.702562,0.0167929]","[-0.755371,-1.43441,2.02297,-0.581487,-0.767256,0.0174955]","[-0.70979,-0.491054,1.31468,2.25931,-0.844268,0.0379639]","[-0.680549,-0.44912,1.21117,2.32224,-0.873493,0.0359359]"]
InbetweenPoses = ["[-1.0023,-1.04478,1.54754,-0.448062,-0.0243877,1.52694]"]
DigitalMiddlePoint = urc.poseToValues("p[-1.011832,0.047732,-0.0871,0.0,0.0,0.0]")


def DoCalibration(write_conn,read_conn):
    urc.syncWrite("movel("+InbetweenPoses[0]+")",write_conn,read_conn)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write_conn,read_conn)

    urc.syncWrite("movel("+MeasurementPoses[0]+")",write_conn,read_conn)
    urc.syncWrite("set_tcp("+ TCP_SENSOR +")",write_conn,read_conn)
    measurement_1 = st.MeasurePoint(write_conn,read_conn,0)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write_conn,read_conn)


    # Take measurement 2: High-Back 2.
    urc.syncWrite("movej("+MeasurementPoses[1]+")",write_conn,read_conn)
    urc.syncWrite("set_tcp("+ TCP_SENSOR +")",write_conn,read_conn)
    measurement_2 = st.MeasurePoint(write_conn,read_conn,1)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write_conn,read_conn)

    # Move through inbetween position.
    urc.syncWrite("movel("+InbetweenPoses[0]+")",write_conn,read_conn)

    # Take measurement 3: Low-Left.
    urc.syncWrite("movel("+MeasurementPoses[2]+")",write_conn,read_conn)
    urc.syncWrite("set_tcp("+ TCP_SENSOR +")",write_conn,read_conn)
    measurement_3 = st.MeasurePoint(write_conn,read_conn,2)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write_conn,read_conn) 

    urc.syncWrite("movel("+MeasurementPoses[3]+")",write_conn,read_conn)
    urc.syncWrite("set_tcp("+ TCP_SENSOR +")",write_conn,read_conn)
    measurement_4 = st.MeasurePoint(write_conn,read_conn,3)
    urc.syncWrite("set_tcp("+ TCP_SCREWDRIVER +")",write_conn,read_conn)

    # Returning back to inbetween position.
    urc.syncWrite("movel("+InbetweenPoses[0]+")",write_conn,read_conn)

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

    out = cal.CalculateOffsets([a,b,c,d],DigitalMiddlePoint)
    # print("Debug: " + str(out[0]) + ", " + str(out[1]) + ", " + str(math.degrees(out[2])))
    return [out[0],out[1],0.0,0.0,0.0,out[2]-math.radians(45)]

total_xy_rz = [0,0,0]
count = 1

# # Start of runtime code.
while True:
    urc.greenLightUR(IP_UR)
    write,read = urc.connectReadWrite(IP_UR,PORT_RECIEVE)

    # Main body.
    Offset =  DoCalibration(write,read)
    total_xy_rz = [total_xy_rz[0] + Offset[0],total_xy_rz[1] + Offset[1],total_xy_rz[2] + Offset[2]]
    print(f'\nAverage variances')
    print(f'--------------------\nX-Axis: {total_xy_rz[0]/count}, Y-Axis: {total_xy_rz[1]/count}, rZ-Axis: {total_xy_rz[2]/count}')
    count = count + 1

    # Close the connection.
    urc.closeReadWrite(write,read)
# # Offset = cal.CalculateOffsets([[-0.920512, 0.0195832, -1.18521], [-0.920497, 0.0667357, -1.1851], [-0.990248, 0.140676, 2.20752], [-1.03219, 0.140834, 2.20742]],[-1.011832,0.047732,-0.0871,0.0,0.0,0.0])
# # print(Offset)
# # print(math.degrees(Offset[5]))

# # Attempt to apply offset to a single point.
# Middle = urc.valuesToPose(DigitalMiddlePoint)
# Point1 = "get_forward_kin([-0.623255, -0.877154, 1.371180, -0.072630, 0.990249, 2.900510])"
# base = "p[0.0,0.0,0.0,0.0,0.0,0.0]"
# CalibrationOffset = urc.valuesToPose(Offset)

