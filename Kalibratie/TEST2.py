import math
import numpy as np

# SIDES_LENGTH = 19.0
# FIRST_CORNER = [0,2]
# DELTA = [1,1]

## Temporarely disabled due to accuracy concerns: By only using one point, any and all faults are multiplied.
# def getSquareFromCorner(delta,position,sidelength):
#     x1,y1 = position[0],position[1]
#     delta = delta[1],-delta[0]
#     x2,y2 = x1+(delta[0]*sidelength),y1+(delta[1]*sidelength)
#     delta = delta[1],-delta[0]
#     x3,y3 = x2+(delta[0]*sidelength),y2+(delta[1]*sidelength)
#     delta = delta[1],-delta[0]
#     x4,y4 = x3+(delta[0]*sidelength),y3+(delta[1]*sidelength)
#     return [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]

#print(getSquareFromCorner(DELTA,FIRST_CORNER,SIDES_LENGTH))

# T2 - Expected positions into measurements.
xp1 = [-1,1]
xp2 = [1,1]
xp3 = [1,-1]
xp4 = [-1,-1]
xcenter = [0,0]

# This is the default test set, these measurements point to a s
J = [0.4104146877838, 0.4104146877838]
K = [0.7506960155965, 0.7506960155965]
I = [-0.6220664717211, 0.6220664717211]
ExpectedCorners = [[-1,0],[0,1],[1,0],[0,-1]]

# # This is a erroring test set: Here, one of the measured lines is perfectly straight, following x=y*0.
# # This causes issues when trying to calculate a coefficient, as this causes a division by 0 error. (It attempts to create a infinitely large coefficient, as it's a straight line up.)
# J = [-0.5,-1]
# K = [0.5,-1]
# I = [-1,0.44]
# ExpectedCorners = [[-1,-1],[-1,1],[1,1],[1,-1]]

# Calculating the first coefficient.
RC_Line1 = (K[1]-J[1])/(K[0]-J[0])

print("RC: "+str(RC_Line1))

# Offset / Translatie van formule.
JKOffset = J[1] - (J[0] * RC_Line1)

print(JKOffset)


# Function for first line.
formulaLine1 = "y = x * "+str(RC_Line1)+" + "+str(JKOffset)

print(formulaLine1)
print("-----------")

## Calculate Formula 2.
# 90 Degrees corner.
# As example:
# y = 2x rotated by 90 degrees becomes x = -2y
# y = ax, x =-ay
# Swap X & Y, a*-1.
try:
    RC_Line2 = -1*(K[0]-J[0])/(K[1]-J[1])
except ZeroDivisionError as err:
    print("[ERROR] Division by Zero found, one of the results are 0, this means one of the two lines have a difference of 0.")
    print("[ERROR] Calculation done: RC_Line2 = -1 * "+ str((K[0]-J[0])) + " / " + str((K[1]-J[1])))
    print("[ERROR] *hl1 scientist scream*")
    exit(0)

print(RC_Line2)

# Offset/Translatie uitrekenen.
IEOffset = I[1] - (I[0]*RC_Line2)

# Formule voor 2de lijn.
formulaLine2 = "y = x * "+str(RC_Line2)+" + "+str(IEOffset)

print("RC: "+str(RC_Line2))
print(IEOffset)
print(formulaLine2)
print("-----------")

a = [[-RC_Line1,1],[-RC_Line2,1]]
b = [JKOffset,IEOffset]
solution = np.linalg.lstsq(a,b,rcond=None)
print("Position of Solution: " + str(solution[0]))
# The solution is in this case the position of the corner.