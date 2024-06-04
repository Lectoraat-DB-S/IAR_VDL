import numpy as np
import math as mt

# Insert measured points into Least squares method.
DataPoints_x = [0,1,2,3]
DataPoints_y = [1,2,3,4]

A = np.vstack([DataPoints_x,np.ones(len(DataPoints_x))]).T
print(A)
m,c = np.linalg.lstsq(A,DataPoints_y,rcond=None)[0]
print(round(m,10))
print(round(c,10))