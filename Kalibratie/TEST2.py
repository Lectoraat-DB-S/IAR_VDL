import math
import numpy as np

# Define division warning as error.
np.seterr(divide = 'raise')

# Which testset to use. (1,2,3,4)
TESTSET = 1

# Digital object positions to determine offsets.
DigitalCentre = [0,0] # Needed component. (Value can be taken from RoboDK export.)
DigitalCorners = [[-1,-1],[-1,1],[1,1],[1,-1]] # Not needed, used for initial debugging.
DigitalAngle = math.radians(45) # Needed component. (Value can be taken from RoboDK export.)


def calcMag(point1,point2):
    return math.sqrt(((float(point2[0])-float(point1[0]))**2) + ((float(point2[1])-float(point1[1]))**2))


# # Test set 1.
if TESTSET == 1:

    J = [0.4104146877838, 0.4104146877838]
    K = [0.7506960155965, 0.7506960155965]
    I = [-0.6220664717211, 0.6220664717211]
    ExpectedCorners = [[-1,1],[0,2],[1,1],[0,0]]
    ExpectedCentre = [0,1]

    MeasuredCorner = "BottomLeft"

elif TESTSET == 2:

    # Test set 2.
    J = [6.6248271655433,6.9167818896378]
    K = [7.5053126404265,6.329791573049]
    I = [5.5906334685221,8.8859502027831]
    ExpectedCorners = [[7,11],[10,9],[8,6],[5,8]]
    ExpectedCentre = [7.5,8.5]

    MeasuredCorner = "BottomLeft"

elif TESTSET == 3:

    # Test set 3.
    J = [-4.1099613345214,4.8900386654786]
    K = [-4.4103326029272,4.5896673970728]
    I = [-5.6325547091728,4.6325547091728]
    ExpectedCorners = [[-5,8],[-3,6],[-5,4],[-7,6]]
    ExpectedCentre = [-5,6]

    MeasuredCorner = "BottomLeft"

elif TESTSET == 4:
    J = [-0.5,-1]
    K = [0.5,-1]
    I = [-1,0.44]
    ExpectedCorners = [[-1,-1],[-1,1],[1,1],[1,-1]]
    ExpectedCentre = [0,0]
    MeasuredCorner = "BottomLeft"
# # This is a erroring test set: Here, one of the measured lines is perfectly straight, following x=y*0.
# # At the current time, the function used to solve the two lines into a point cannot handle a inf (Infinite number) as input.


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
    RC_Line2 = math.inf

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
try:
    solution = np.linalg.lstsq(a,b,rcond=None)
except Exception as err:
    if err.args[0]=="SVD did not converge in Linear Least Squares":
        print("[ERROR] SVD Did not converge, assuming one RC is infinite.")
        if RC_Line1==math.inf:
            solution = [K[0],I[1]],[]
        elif RC_Line2==math.inf:
            solution = [I[0],K[1]],[]
        else:
            print("[ERROR] Unable to fix, exiting.")
            exit(1)
    else:
        exit(1)

print("Position of Solution: " + str(solution[0]))
# The solution is in this case the position of the corner.
Corner = solution[0]

# Calculating the middle of the square through this corner.
# Move with a magnitude of half the length along line 1 or 2.
# For the actual ordeal, this will be 95mm.
travel = calcMag(ExpectedCorners[0],ExpectedCorners[1]) / 2
angle = math.atan(RC_Line1)
delta = [round(math.cos(angle)*travel,10),round(math.sin(angle)*travel,10)]
stepOne = [round(Corner[0]+delta[0],10),round(Corner[1]+delta[1],10)]
print("-EK-1-")
print("Corner: "+str(Corner))
print("Travel: "+str(travel))
print("Angle: " + str(math.degrees(angle)))
print("Delta: " + str(delta))
print("Step position: " + str(stepOne))
print("------")

# Due to current setup, we can use RC_Line2 as the 90 degree rotation.
angle = math.atan(RC_Line2)
if angle<0:
    delta = [round(math.sin(angle)*travel,10),round(math.cos(angle)*travel,10)] # Works for test set 1 and 3
else:
    delta = [round(math.cos(angle)*travel,10),round(math.sin(angle)*travel,10)] # Works for test set 2 and 4.

# Dot product time?
# D(a,b) = a.x * b.x + a.y * b.y
# R = D(A,(0,1))


Centre = [round(stepOne[0]+delta[0],10),round(stepOne[1]+delta[1],10)]
print("-EK-2-")
print("Travel: "+str(travel))
print("Angle: " + str(math.degrees(angle)))
print("Delta: " + str(delta))
print("Step position: " + str(Centre))
print("------")

print("------------Final Data------------")
print("Centre: " + str(Centre) + "\t| Expected Centre: " + str(ExpectedCentre))
print("Corner: " + str(Corner) + "\t| Expected Corners: " + str(ExpectedCorners))
print("Testset: " + str(TESTSET))
print("----------------------------------")


# Calculate angle of vector between corner and middle against the Y-axis.
try:
    RC_CentreToCorner = (Centre[1]-Corner[1])/(Centre[0]-Corner[0])
except FloatingPointError as err:
    RC_CentreToCorner = math.inf
angle = math.atan(RC_CentreToCorner)
print("Hoek via atan: " + str(math.degrees(angle)))

# Calculate offsets.
Positional_Offset = [Centre[0]-DigitalCentre[0],Centre[1]-DigitalCentre[1]]
Rotational_Offset = angle-DigitalAngle

print("Positional Offset: " + str(Positional_Offset))
print("Rotational Offset: " + str(math.degrees(Rotational_Offset)))

# With these two values, one should be able to modify the centre point of the exported path (by moving and rotating said point), making the generated path automatically move with it.
