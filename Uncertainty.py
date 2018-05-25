import numpy as np
from math import sqrt, pi
import matplotlib.pyplot as plt

def Volumes(V1, V2, rad, H, P1, P2, M):
    '''

    :param V1: Volume 1 of Pycno
    :param V2: Volume 2 of Pynco
    :param rad: Radius of firn cylinder
    :param H: Height of firn cylinder
    :param P1: Pressure before relaxation
    :param P2: Pressure after relaxation
    :param M: Mass of firn sample
    :return: Volume of closed pores (Vcl), Volume of open pores (Vop)
    '''

    pice = .9167 # ice density

    R = P2/P1
    Vs = V1 - (R/(1-R)) * V2
    Vice = M/pice
    Vtot = pi * (rad**2) * H

    # Compute closed and open porosity
    Vcl = Vs - Vice
    Vop = Vtot - Vs

    return Vop, Vcl, Vtot - Vice


# Load Pycno Volumes
f = open('Volumes_Pycno.txt')
f.readline()
l = f.readline()
l = l.split()
V1, V2 = float(l[0]), float(l[1])

# # Read other parameters
# rad = 4.8/2.  # Radius in cm
# H = 4.608    # Height in cm
# P1 = 847.91 # Pressure before relaxation
# P2 = 751.49 # Pressure after
# M= 70.953    # Mass in g

rad = 3.38/2.  # Radius in cm
H = 5.06    # Height in cm
P1 = 989.20 # Pressure before relaxation
P2 = 922.68 # Pressure after
M= 35.850    # Mass in g

# Compute porosity volumes
pice = .9167
args = [V1, V2, rad, H, P1, P2, M]
Vop, Vcl, Vptot = Volumes(*args)

# -------------------------------------------------------------------------
# Construct Jacobian matrix (matrix of derivatives)
# -------------------------------------------------------------------------

Jac = np.matrix(np.zeros((2,7)))
# Loop over 7 different inputs
for j in range(7):
    # Construct new list of parameters with a small variation in the j-th
    args_s = np.array(args)
    darg = args_s[j]/100000.
    args_s[j] += darg
    args_s = list(args_s)

    # Compute resulting closed and open porosities
    Vo2, Vc2, dum = Volumes(*args_s)
    # Estimate derivative
    dero = (Vo2 - Vop)/darg
    derc = (Vc2 - Vcl)/darg

    # Store in Jacobian matrix
    Jac[0,j] = dero
    Jac[1,j] = derc

# -------------------------------------------------------------------------
# Construct Covariance matrix of input parameters
#  -------------------------------------------------------------------------

CoVar = np.matrix(np.zeros((7,7)))
CoVar[0,0] = 0.2293849482788453**2     # V1
CoVar[1,1] = 0.014303077508242902**2  # V2
CoVar[2,2] = 0.05**2                  # Radius
CoVar[3,3] = 0.05**2                   # Height
CoVar[4,4] = 0.5**2                    # P1
CoVar[5,5] = 0.5**2                    # P1
CoVar[6,6] = 0.012**2                  # Mass

CoVar[0,1] = 0.00324571455419
CoVar[1,0] = 0.00324571455419

# -------------------------------------------------------------------------
# Compute uncertainties
#  -------------------------------------------------------------------------
Uncer = np.matmul(np.matmul(Jac, CoVar), Jac.transpose())
Uncers_op = np.zeros(7)
Uncers_cl = np.zeros(7)
for i in range(7):
    Uncers_op[i] = sqrt( (Jac[0,i]**2) * CoVar[i,i] )
    Uncers_cl[i] = sqrt( (Jac[1,i]**2) * CoVar[i,i] )

plt.bar(list(range(7)), Uncers_op)
plt.show()
plt.bar(list(range(7)), Uncers_cl)
plt.show()



print('Open Porosity:', Vop, 'cm3 with uncertainty', sqrt(Uncer[0,0]))
print('Closed Porosity:', Vcl, 'cm3 with uncertainty', sqrt(Uncer[1,1]))
print('Total Porosity:', Vptot, 'cm3')