import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import os


'''Script to calibrate pycno
Need an input file with Volume, P1, P2
'''

# Load relaxation file
folder = '/media/fourteau/KevinF/Data/Pycno/Calibration'
name = 'calib_froid.txt'
filename = os.path.join(folder, name)
Vballs, P1, P2 = np.loadtxt(filename,unpack=True) # Vcalib: Calibration balls
Rs = P2/P1 # Compute R=P2/P1

Nrelax = len(Vballs) # Number of relaxation

# Construct X matrix
#  ---         ---
#  | 1   -(R/1-R) |
#  | .        .   |
#  | .        .   |
#  | .        .   |
#  | .        .   |
#  | 1   -(R/1-R) |
#  ---         ---
for r in Rs:
    try : X = np.vstack([X,np.array([1,-r/(1-r)])]) # If X already exists stack a new row
    except: X = np.matrix(np.array([1, -r/(1-r)]))  # If not create matrix with a 1st row

# Solve to find best parameters and store in res
R = np.matmul(np.transpose(X),X)
inv = np.linalg.inv(R)
res = np.matmul(np.matmul(inv,np.transpose(X)), np.transpose(Vballs))

# Compute volume estimates
Vest = np.transpose(np.matmul(X, res.transpose()))

# Estimate uncertainties
std_balls = np.sqrt(np.sum((np.array(Vest - Vballs)**2))/(Nrelax-1))
Var_mat = (std_balls**2) * np.linalg.inv(np.matmul(np.transpose(X),X)) # Covariance Matrix

# Print Result
print('V1 =', res[0,0], '+/-', sqrt(Var_mat[0,0]))
print('V2 =', res[0,1], '+/-', sqrt(Var_mat[1,1]))
print('Covariance =', Var_mat[1,0])

# Plot theoretical VS estimate results
plt.scatter(Vballs, np.array(Vest)[0])
plt.plot([0,50],[0,50], ls='--', c='k')
plt.xlabel('Theoretical Volume')
plt.ylabel('Estimate Volume')
plt.show()

f = open(os.path.join(folder, 'Volumes_pycno.txt'), 'w')
f.write('#V1\tV2\n')
f.write(str(res[0,0]) +'\t'+ str(res[0,1])+'\n')
f.write(str(Var_mat[0,0]) +'\t'+ str(Var_mat[1,1]) +'\t'+ str(Var_mat[1,0]))
f.close()




