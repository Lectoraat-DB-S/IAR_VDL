import math
import numpy as np

np.seterr(divide='raise')

# Variables, WIP - Move generic ones over to main.py.
DigitalCentre = [0,0]
DigitalAngle = math.radians(45)

CORNER = "TopRight"

# Length of the sides in m.
SIDELENGTH = 0.19
# -----------------------

def CalculateMagnitude(point_1,point_2):
    return math.sqrt(((float(point_2[0])-float(point_1[0]))**2) + ((float(point_2[1])-float(point_1[1]))**2))

def CalculateOffsets(measurement_points_abc,digital_middlepoint):
    """ A function to calculate the offsets of a square drawn along the 3 measurement points, compared to the digital middlepoint.
    
    \param [in] measurement_points_abc A array of 3 points, only containing their x,y and rz values.
    \param [in] digital_middlepoint A array containing the x,y,z,rx,ry and rz values of the digital middlepoint. (Can be made by turning the pose-string into values with "urc.poseToValues()")
    """
    A = measurement_points_abc[0] #J
    B = measurement_points_abc[1] #K
    C = measurement_points_abc[2] #I

    # Calculating the first coefficient and offset, giving us the full formula of the first line.
    coefficient_1 = (B[1]-A[1])/(B[0]-A[0])
    offset_1 = A[1] - (A[0] * coefficient_1)

    # Calculating the second coefficient and offset, derived from the first formula.
    try:
        coefficient_2 = -1*(B[0]-A[0])/(B[1]-A[1])
    except ZeroDivisionError as err:
        coefficient_2 = math.inf

    # Calculating the offset.
    if coefficient_2 == math.inf:
        offset_2 = C[0]
    else:
        offset_2 = C[1] - (C[0]*coefficient_2)
    
    try:
        lstsq = np.linalg.lstsq([[-coefficient_1,1],[-coefficient_2,1]],[offset_1,offset_2],rcond=None)
    except Exception:
        if coefficient_1==math.inf:
            lstsq = [B[0],C[1]],[]
        elif coefficient_2==math.inf:
            lstsq = [C[0],B[1]],[]
        else:
            print("[ERROR] Error in has no predefined solution, exiting.")
            exit(1)
    corner_point = lstsq[0]

    # Calculating the middle of the square through the previously calculated lines.
    # First step, along Line 1.
    travel_length = SIDELENGTH/2

    angle_1 = math.atan(coefficient_1)
    if CORNER=="TopRight":
        if angle_1<0:
            delta_1 = [1*(math.cos(angle_1)*travel_length),1*(math.sin(angle_1)*travel_length)]
        else:
            delta_1 = [1*(math.cos(angle_1)*travel_length),-1*(math.sin(angle_1)*travel_length)]
    else:
        print("[ERROR] Corner not prepared yet.")
        exit(1)
    centre_point = [corner_point[0]+delta_1[0],corner_point[1]+delta_1[1]]

    # 2nd step, along Line 2.
    angle_2 = math.atan(coefficient_2)

    if CORNER=="TopRight":
        delta_2 =  [-1*(math.cos(angle_2)*travel_length),1*(math.sin(angle_2)*travel_length),10]
    else:
        print("[ERROR] Corner not prepared yet.")
        exit(1)
    centre_point = [round(centre_point[0]+delta_2[0],10),round(centre_point[1]+delta_2[1],10)]

    try:
        diagonal = (centre_point[1]-corner_point[1])/(centre_point[0]-corner_point[0])
    except FloatingPointError:
        diagonal = math.inf
    rz_offset = math.atan(diagonal)

    # Output is X, Y and rZ in Radians. [X,Y,rZ]
    offset_x_y_rz = [digital_middlepoint[0]-centre_point[0],digital_middlepoint[1]-centre_point[1],digital_middlepoint[5]-rz_offset]

    # Debugging section
    # print("--------Calibration Debug--------------")
    # print("Travel: " + str(travel_length))
    # print("CE1: " + str(coefficient_1) + ", CE2: " + str(coefficient_2))
    # print("Offset 1: " + str(offset_1) + ", Offset 2: " + str(offset_2))
    # print()
    # print("Corner point: " + str(corner_point))
    # print()
    # print("Delta 1: " + str(delta_1) + ", Delta 2: " + str(delta_2))
    # print("Angle_1: " + str(math.degrees(angle_1)) + ", Angle_2: " + str(math.degrees(angle_2)))
    # print("Angle_1 Cos: " + str(math.cos(angle_1)) + ", Angle_2 Cos: " + str(math.cos(angle_2)))
    # print("Angle_1 Sin: " + str(math.sin(angle_1)) + ", Angle_2 sin: " + str(math.sin(angle_2)))
    # print("Offsets: " + str(offset_x_y_rz))
    # print("--------End of Calibration Debug-------")
    # print("\n")
    return offset_x_y_rz