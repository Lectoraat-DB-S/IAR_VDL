import numpy as np
import math as mt

# Insert measured points into Least squares method.
DataPoints_x1 = [0,1]
DataPoints_y1 = [1,2]

DataPoints_x2 = [0,1]
DataPoints_y2 = [3,2]

A1 = np.vstack([DataPoints_x1,np.ones(len(DataPoints_x1))]).T
m1,c1 = np.linalg.lstsq(A1,DataPoints_y1,rcond=None)[0]

A2 = np.vstack([DataPoints_x2,np.ones(len(DataPoints_x2))]).T
m2,c2 = np.linalg.lstsq(A2,DataPoints_y2,rcond=None)[0]

result = [(c2-c1)/(m1-m2)]
result = [round(result[0],8),round(m1*result[0]+c1,8)]

print(A1)
print(A2)
print("--- Line 1")
print(round(m1,10))
print(round(c1,10))
print("--- Line 2")
print(round(m2,10))
print(round(c2,10))
print("----------")
print(result)