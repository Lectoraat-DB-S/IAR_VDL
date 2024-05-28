import math
import numpy as np

np.seterr(divide='raise')

# Variables, WIP - Move generic ones over to main.py.
DigitalCentre = [0,0]
DigitalAngle = math.radians(45)

# Length of the sides in m.
SideLength = 0.095
# -----------------------

def CalculateMagnitude(point_1,point_2):
    return math.sqrt(((float(point_2[0])-float(point_1[0]))**2) + ((float(point_2[1])-float(point_1[1]))**2))

def CalculateOffsets(measurement_points_abc):
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

    # Bereken de offset.
    if coefficient_2 == math.inf:
        offset_2 = C[0]
    else:
        offset_2 = C[1] - (C[0]*coefficient_2)
    
    try:
        lstsq = np.linalg.lstsq([[-coefficient_1,1],[-coefficient_2,1]],[offset_1,offset_2],rcond=None)
    except Exception as err:
        if coefficient_1==math.inf:
            lstsq = [B[0],C[1]],[]
        elif coefficient_2==math.inf:
            lstsq = [C[0],B[1]],[]
        else:
            print("[ERROR] Error in has no predefined solution, exiting.")
            exit(1)
    corner_point = lstsq[0]

    # Calculating the middle of the square through the previously calculated lines.
    # First line.
    travel_length = SideLength/2
    angle_1 = math.atan(coefficient_1)
    delta_1 = [round(math.cos(angle_1)*travel_length,10),round(math.sin(angle_1)*travel_length,10)]
    centre_point = [round(corner_point[0]+delta_1[0],10),round(corner_point[1]+delta_1[1],10)]

    # 2nd line.
    angle_2 = math.atan(coefficient_2)
    if angle_2 < 0:
        

    # Output is X, Y and rZ in Radians. [X,Y,rZ]
    offset_x_y_rz = [0,0,0]
    return offset_x_y_rz