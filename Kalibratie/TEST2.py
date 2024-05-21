import math
import numpy as np

SIDES_LENGTH = 19.0
FIRST_CORNER = [0,2]
DELTA = [1,1]

def getSquareFromCorner(delta,position,sidelength):
    x1,y1 = position[0],position[1]
    delta = delta[1],-delta[0]
    x2,y2 = x1+(delta[0]*sidelength),y1+(delta[1]*sidelength)
    delta = delta[1],-delta[0]
    x3,y3 = x2+(delta[0]*sidelength),y2+(delta[1]*sidelength)
    delta = delta[1],-delta[0]
    x4,y4 = x3+(delta[0]*sidelength),y3+(delta[1]*sidelength)
    return [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]

#print(getSquareFromCorner(DELTA,FIRST_CORNER,SIDES_LENGTH))

# T2 - Expected positions into measurements.
xp1 = [-1,1]
xp2 = [1,1]
xp3 = [1,-1]
xp4 = [-1,-1]
xcenter = [0,0]

J = [0.4104146877838, 0.4104146877838]
K = [0.7506960155965, 0.7506960155965]
I = [-0.6220664717211, 0.6220664717211]

# J = [-0.5,-1]
# K = [0.5,-1]
# I = [-1,0.44]

## Calculate Formula 1.

# Richtings-coëfficient.
RC_Line1 = (K[1]-J[1])/(K[0]-J[0])

print("RC: "+str(RC_Line1))

# Offset / Translatie van formule.
JKOffset = J[1] - (J[0] * RC_Line1)

print(JKOffset)

# Formule voor 1ste lijn.
formulaLine1 = "y = x * "+str(RC_Line1)+" + "+str(JKOffset)

print(formulaLine1)
print("-----------")
## Calculate Formula 2.
# 90 Graden hoek.
RC_Line2 = RC_Line1 * -1
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


