import math
import numpy as np
import os # For formatting the prints.

np.seterr(divide='raise')

CORNER = "TopRight"

# Length of the sides in m.
SIDELENGTH = 0.19
# -----------------------

def CalculateMagnitude(point_1,point_2):
    return math.sqrt(((float(point_2[0])-float(point_1[0]))**2) + ((float(point_2[1])-float(point_1[1]))**2))

def CalculateOffsets(measurement_points_abcd,digital_middlepoint):
    """ A function to calculate the offsets of a square drawn along the 3 measurement points, compared to the digital middlepoint.
    
    \param [in] measurement_points_abc A array of 3 points, only containing their x,y and rz values.
    \param [in] digital_middlepoint A array containing the x,y,z,rx,ry and rz values of the digital middlepoint. (Can be made by turning the pose-string into values with "urc.poseToValues()")
    """
    A = measurement_points_abcd[0]
    B = measurement_points_abcd[1] 
    C = measurement_points_abcd[2] 
    D = measurement_points_abcd[3] 

    # Adding 45 degrees to rZ offset, in order to compensate for the method used to get the offset angle. (If the object's rotation is 0, it will measure it as 45. (Inverse tangent of 1 or -1.)
    digital_middlepoint[5] = digital_middlepoint[5]+math.radians(45)

    # See Mark's feedback, using lstsq to calculate the lines instead of manually.
    # Put the point data together in arrays.
    measurements_line1_x = [A[0],B[0]]
    measurements_line2_x = [C[0],D[0]]
    measurements_line1_y = [A[1],B[1]]
    measurements_line2_y = [C[1],D[1]]

    # Put x points of line 1 and 2 in a vertical matrix, pairing each with a 1.
    A1 = np.vstack([measurements_line1_x,np.ones(len(measurements_line1_x))]).T
    A2 = np.vstack([measurements_line2_x,np.ones(len(measurements_line2_y))]).T
    m1,c1 = np.linalg.lstsq(A1,measurements_line1_y,rcond=None)[0]
    m2,c2 = np.linalg.lstsq(A2,measurements_line2_y,rcond=None)[0]

    x_intersect = (c2-c1)/(m1-m2)
    corner_point = [x_intersect,m1*x_intersect+c1]

    # Calculating the middle of the square through the previously calculated lines.
    # First step, along Line 1.
    travel_length = SIDELENGTH/2

    angle_1 = math.atan(m1)
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
    angle_2 = math.atan(m2)

    if CORNER=="TopRight":
        delta_2 =  [-1*(math.cos(angle_2)*travel_length),1*(math.sin(angle_2)*travel_length),10]
    else:
        print("[ERROR] Corner not prepared yet.")
        exit(1)
    centre_point = [round(centre_point[0]+delta_2[0],10),round(centre_point[1]+delta_2[1],10)]

    A3 = np.vstack([[centre_point[0],corner_point[0]],np.ones(2)]).T
    m3,c3 = np.linalg.lstsq(A3,[centre_point[1],corner_point[1]],rcond=None)[0]
    diagonal = math.atan(m3)
    rz_offset = diagonal

    ## Debug prints for angle.
    # print(rz_offset)
    # print(digital_middlepoint[5])

    # Output is X, Y and rZ in Radians. [X,Y,rZ]

    
    offset_x_y_rz = [centre_point[0]-digital_middlepoint[0]+0.0032521844999999455,centre_point[1]-digital_middlepoint[1]+0.0024827895142857104,rz_offset-digital_middlepoint[5]]

    # Debugging section.
    os.system('cls')
    print("--------------------- Calibration Results ----------------------")
    print("\n")
    print("X-Axis offset: " + str(round(offset_x_y_rz[0]*1000,2)) + "mm\t Y-Axis offset: " + str(round(offset_x_y_rz[1]*1000,2)) + "mm\t Z-rotation offset: " + str(round(math.degrees(offset_x_y_rz[2]),3)) + " degrees.")
    print("\n")
    print("Raw data:")
    print(f'Expected Centre point: {digital_middlepoint}\tMeasured Centre point: {centre_point}')
    print(f'Corner point: {corner_point}')
    print("\n")
    # print(f'Line 1 formula: y = {round(m1,1)}x + {round(c1,1)}\tLine 2 formula: y = {round(m2,1)}x + {round(c2,1)}')

    return offset_x_y_rz