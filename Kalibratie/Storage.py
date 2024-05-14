import URCommunication as urc
import time
import csv
import math

measuredCounter = 0

# def retrievePoint()

def MeasurePoint(write_conn,read_conn):
    global measuredCounter
    curPose = urc.readWrite("get_actual_tcp_pose()",write_conn,read_conn)
    print(curPose)
    urc.asyncWrite("measure_point()",write_conn)
    while urc.read(read_conn) == 1:
        print("Waiting...")
    print("Done")
    time.sleep(1)
    measuredPoint = urc.readWrite("get_actual_tcp_pose()",write_conn,read_conn)
    print("[COBOT] Position is: " + measuredPoint)
    urc.syncWrite("movel(" + curPose + ",a=1.2,v=0.25,t=0,r=0)",write_conn,read_conn)

    # Format the pose (string) variable into a array of smaller strings for each value.
    startPose = (curPose.replace("p[",'')).split(",")
    endPose = (measuredPoint.replace("p[",'')).split(",")

    # Calculate the Magnitude of the made motion.
    Magnitude = math.sqrt(((float(endPose[0])-float(startPose[0]))**2) + ((float(endPose[1])-float(startPose[1]))**2) + ((float(endPose[2])-float(startPose[2]))**2))

    # Attempt to write the measured point to storage. This is appended, regardless if the file already contains a point with the same name.
    try:
        with open("Kalibratie/Measurements/points.csv", mode="a", newline = '') as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(["Point" + str(measuredCounter),measuredPoint])
            measuredCounter = measuredCounter + 1
    except Exception as err:
        print(err)

    return Magnitude

def MeasureEdge(write_conn,read_conn):
    urc.asyncWrite("measure_edge()",write_conn)
    while urc.read(read_conn) == 1:
        print("Waiting...")
    print("Done")

    # DEBUG
    basePose = urc.read(read_conn)
    currentPose = urc.read(read_conn)
    print(basePose)
    print(currentPose)

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
