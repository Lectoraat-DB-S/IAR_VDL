import math
import numpy as np

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
    E = measurement_points_abcd[4]
    F = measurement_points_abcd[5]
    G = measurement_points_abcd[6]
    H = measurement_points_abcd[7]

    # See Mark's feedback, using lstsq to calculate the lines instead of manually.
    # Put the point data together in arrays.
    measurements_line1_x = [A[0],B[0]]
    measurements_line2_x = [C[0],D[0]]
    measurements_line1_y = [A[1],B[1]]
    measurements_line2_y = [C[1],D[1]]
    measurements_line3_x = [E[0],F[0]]
    measurements_line3_y = [E[1],F[1]]
    measurements_line4_x = [G[0],H[0]]
    measurements_line4_y = [G[1],H[1]]

    # Put x points of line 1 and 2 in a vertical matrix, pairing each with a 1.
    A1 = np.vstack([measurements_line1_x,np.ones(len(measurements_line1_x))]).T
    A2 = np.vstack([measurements_line2_x,np.ones(len(measurements_line2_x))]).T
    A3 = np.vstack([measurements_line3_x,np.ones(len(measurements_line3_x))]).T
    A4 = np.vstack([measurements_line4_x,np.ones(len(measurements_line4_x))]).T
    m1,c1 = np.linalg.lstsq(A1,measurements_line1_y,rcond=None)[0]
    m2,c2 = np.linalg.lstsq(A2,measurements_line2_y,rcond=None)[0]
    m3,c3 = np.linalg.lstsq(A3,measurements_line3_y,rcond=None)[0]
    m4,c4 = np.linalg.lstsq(A4,measurements_line4_y,rcond=None)[0]

    x_intersect_1 = (c2-c1)/(m1-m2)
    x_intersect_2 = (c3-c2)/(m2-m3)
    x_intersect_3 = (c4-c3)/(m3-m4)
    x_intersect_4 = (c1-c4)/(m4-m1)

    corner_point_1 = [x_intersect_1,m1*x_intersect_1+c1]
    corner_point_2 = [x_intersect_2,m2*x_intersect_2+c2]
    corner_point_3 = [x_intersect_3,m3*x_intersect_3+c3]
    corner_point_4 = [x_intersect_4,m4*x_intersect_1+c4]

    # Calculating the middle of the square through the previously calculated lines.
    # First step, along Line 1.
    
    centre_point = [(corner_point_1[0]+corner_point_2[0]+corner_point_3[0]+corner_point_4[0])/4,(corner_point_1[1]+corner_point_2[1]+corner_point_3[1]+corner_point_4[1])/4]

    DIAG = np.vstack([[centre_point[0],corner_point_1[0]],np.ones(2)]).T
    DIAG_m,DIAG_c = np.linalg.lstsq(DIAG,[centre_point[1],corner_point_1[1]],rcond=None)[0]
    diagonal = math.atan(DIAG_m)
    rz_offset = diagonal

    ## Debug prints for angle.
    # print(rz_offset)
    # print(digital_middlepoint[5])

    # Output is X, Y and rZ in Radians. [X,Y,rZ]
    offset_x_y_rz = [centre_point[0]-digital_middlepoint[0],centre_point[1]-digital_middlepoint[1],rz_offset-digital_middlepoint[5]]

    return offset_x_y_rz