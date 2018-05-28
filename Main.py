import numpy as np
from math import sqrt, pi
import matplotlib.pyplot as plt
import os

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

# -------- PARAMETERS TO FILL ------
dP = 0.1   # Uncertainty on Pressures
dM = 0.01  # Uncertainty on Mass
# ------------------------------------

# Load Pycno Volumes
folder = '/media/fourteau/KevinF/Data/Pycno/Calibration'
f = open(os.path.join(folder, 'Volumes_pycno.txt'))
f.readline()
l = f.readline()
l = l.split()
V1, V2 = float(l[0]), float(l[1])
l = f.readline()
l = l.split()
dV1, dV2, covV1V2 = float(l[0]), float(l[1]), float(l[2])

# # Read other parameters
folder ='/media/fourteau/KevinF/Data/Pycno/Measurments'
file = '20180524.txt'
filename = os.path.join(folder, file)
Data = np.loadtxt(filename)
Vops = np.array([])
Vcls = np.array([])
Depths = np.array([])

Out_array = np.array([])


for i in range(Data.shape[0]):

    Depth = Data[i,0]
    P1 = Data[i, 1]
    P2 = Data[i, 2]
    rad = Data[i, 3]/2.
    H = Data[i, 4]
    M = Data[i, 5]
    dr = Data[i, 6]
    dh = Data[i, 7]
    # Compute porosity volumes
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
    CoVar[0,0] = dV1     # V1
    CoVar[1,1] = dV2  # V2
    CoVar[2,2] = dr**2                  # Radius
    CoVar[3,3] = dh**2                   # Height
    CoVar[4,4] = dP**2                    # P1
    CoVar[5,5] = dP**2                    # P2
    CoVar[6,6] = dM**2                  # Mass

    CoVar[0,1] = covV1V2
    CoVar[1,0] = covV1V2

    # -------------------------------------------------------------------------
    # Compute uncertainties
    #  -------------------------------------------------------------------------
    Uncer = np.matmul(np.matmul(Jac, CoVar), Jac.transpose())

    try: Out_array = np.vstack((Out_array, np.array([Depth, Vop, sqrt(Uncer[0,0]), Vcl, sqrt(Uncer[1,1]) ])))
    except: Out_array = np.array([Depth, Vop, sqrt(Uncer[0,0]), Vcl, sqrt(Uncer[1,1]) ])

    print('--------- SAMPLE', i+1, '-------------')
    print('Open Porosity:', Vop, 'cm3 with uncertainty', sqrt(Uncer[0,0]))
    print('Closed Porosity:', Vcl, 'cm3 with uncertainty', sqrt(Uncer[1,1]))
    print('Total Porosity:', Vptot, 'cm3')

fig = plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax1.errorbar(Out_array[:,0], Out_array[:,1], yerr=Out_array[:,2], color='steelblue', fmt='o', ecolor='#a7cbd5')
ax2.errorbar(Out_array[:,0], Out_array[:,3], yerr=Out_array[:,4], color='orange', fmt='o', ecolor='#ffee88')
ax1.set_ylabel('Open Porosity')
ax2.set_ylabel('Closed Porosity')
ax1.set_xlabel('Depth')
# ax1.grid(True)
plt.show()

fig = plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(111)
ax1.scatter(Out_array[:,0], Out_array[:,3]/(Out_array[:,1]+Out_array[:,3]), color='steelblue')
ax1.set_ylabel('Closed/Total Porosity')
ax1.set_xlabel('Depth')
# ax1.grid(True)
plt.show()


header = 'Depth\tVop\tdVop\tVcl\tdVcl'
np.savetxt(os.path.join(folder, file.split('.')[0] + '_results.txt'), Out_array, header=header)