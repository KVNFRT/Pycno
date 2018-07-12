import numpy as np
from math import sqrt, pi
import matplotlib.pyplot as plt
import  matplotlib as mpl
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

    return Vop, Vcl, Vop + Vcl

# -------- PARAMETERS TO FILL ------
dP = 0.1   # Uncertainty on Pressures
dM = 0.01  # Uncertainty on Mass
fact = .15 # Fraction of pore open with lathe
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

# # Read measurement file
folder ='/media/fourteau/KevinF/Data/Pycno/Measurments'
file = '20180524.txt'
filename = os.path.join(folder, file)
Data = np.loadtxt(filename)
Vops = np.array([])
Vcls = np.array([])
Depths = np.array([])

Out_array = np.array([])
times = np.array([])

for i in range(Data.shape[0]):

    Depth = Data[i,0]
    t = round(Data[i, 1]) + (Data[i,1] - round(Data[i,1]))/.60
    P1 = Data[i, 2]
    P2 = Data[i, 3]
    rad = Data[i, 4]
    H = Data[i, 5]
    M = Data[i, 6]
    dr = Data[i, 7]
    dh = Data[i, 8]

    # Compute porosity volumes
    args = [V1, V2, rad, H, P1, P2, M]
    Vop, Vcl, Vptot = Volumes(*args)
    Vtot = pi * H * rad**2
    dens = M/Vtot

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
    CoVar[0,0] = dV1                    # V1
    CoVar[1,1] = dV2                    # V2
    CoVar[2,2] = dr**2                  # Radius
    CoVar[3,3] = dh**2                  # Height
    CoVar[4,4] = dP**2                  # P1
    CoVar[5,5] = dP**2                  # P2
    CoVar[6,6] = dM**2                  # Mass

    CoVar[0,1] = covV1V2
    CoVar[1,0] = covV1V2

    # -------------------------------------------------------------------------
    # Compute uncertainties
    #  -------------------------------------------------------------------------
    Uncer = np.matmul(np.matmul(Jac, CoVar), Jac.transpose())

    if Vcl>0:
        Vcl_cor = min(Vcl / (1-fact), Vptot) # Correct closed porosity but limit to Vptot max
    else:
        Vcl_cor = Vcl
    Vop_cor = Vptot - Vcl_cor

    try: Out_array = np.vstack((Out_array, np.array([Depth, Vop, Vop_cor, sqrt(Uncer[0,0]), Vcl, Vcl_cor, sqrt(Uncer[1,1]), Vptot, dens, Vtot ])))
    except: Out_array = np.array([Depth, Vop, Vop_cor, sqrt(Uncer[0,0]), Vcl, Vcl_cor, sqrt(Uncer[1,1]), Vptot, dens, Vtot ])

    times = np.append(times, t)

    print('--------- SAMPLE', i+1, '-------------')
    print('Open Porosity:', Vop_cor, 'cm3 with uncertainty', sqrt(Uncer[0,0]))
    print('Closed Porosity:', Vcl_cor, 'cm3 with uncertainty', sqrt(Uncer[1,1]))
    print('Total Porosity:', Vptot, 'cm3')

idep = 0
iVop = 1
iVopc = 2
iVcl = 4
iVclc = 5
iVpt = 7
idens = 8
iVtot = 9

# ----------- PLOT ------------

# Plot Open and Closed porosity VS Depth
fig = plt.figure(figsize=(14,6))
fig.subplots_adjust(top=.95,bottom=.1,left=.05,right=1.00)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
sc = ax1.scatter(Out_array[:,idep], Out_array[:,iVopc]/Out_array[:,iVpt], s=100, c=times, marker='o', cmap='viridis', edgecolor='#050505')
ax2.scatter(Out_array[:,idep], Out_array[:,iVclc]/Out_array[:,iVpt], s=100, c=times, marker='s', cmap='viridis', edgecolor='#050505')
cax = fig.colorbar(sc)
cax.set_label('Time')
ax1.set_ylabel('Open Porosity / Total Porosity Volume')
ax2.set_ylabel('Closed Porosity / Total Porosity Volume')
ax1.set_xlabel('Depth (m)')
# ax1.grid(True)
plt.show()

# Plot Closed/Total porosity VS Depth
fig = plt.figure(figsize=(14,6))
fig.subplots_adjust(top=.95,bottom=.1,left=.05,right=1.00)
ax1 = fig.add_subplot(111)
sc = ax1.scatter(Out_array[:,idep], Out_array[:,iVclc]/Out_array[:,iVpt], s=100, c=times, marker='o', cmap='viridis', edgecolor='#050505')
cax = fig.colorbar(sc)
cax.set_label('Time')
ax1.set_ylabel('Closed/Total Porosity (cm3)')
ax1.set_xlabel('Depthy (m)')
# ax1.grid(True)
plt.show()

# Plot Open and Closed porosity VS Density
fig = plt.figure(figsize=(14,6))
fig.subplots_adjust(top=.95,bottom=.1,left=.05,right=1.00)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
sc = ax1.scatter(Out_array[:,idens], Out_array[:,iVopc]/Out_array[:,iVpt], s=100, c=Out_array[:,0], marker='o', cmap='viridis', edgecolor='#050505')
ax2.scatter(Out_array[:,-2], Out_array[:,iVclc]/Out_array[:,iVpt], s=100, c=Out_array[:,0], marker='s', cmap='viridis', edgecolor='#050505')
cax = fig.colorbar(sc)
cax.set_label('Depth (m)')
ax1.set_ylabel('Open Porosity (cm3)')
ax2.set_ylabel('Closed Porosity (cm3)')
ax1.set_xlabel('Density (g/cm3)')
# ax1.grid(True)
plt.show()

# Plot Closed/Total porosity VS Density
fig = plt.figure(figsize=(14,6))
fig.subplots_adjust(top=.95,bottom=.1,left=.05,right=1.00)
ax1 = fig.add_subplot(111)
sc = ax1.scatter(Out_array[:,idens], Out_array[:,iVclc]/Out_array[:,iVpt], s=100, c=Out_array[:,0], marker='o', cmap='viridis', edgecolor='#050505')
cax = fig.colorbar(sc)
cax.set_label('Depth (m)')
ax1.set_ylabel('Closed/Total Porosity (cm3)')
ax1.set_xlabel('Density (g/cm3)')
# ax1.grid(True)
plt.show()

# Save data
header = 'Depth\tVop(cm3)\tVop_cor(cm3)\tdVop(cm3)\tVcl(cm3)\tVcl_cor(cm3)\tdVcl(cm3)\tVptot(cm3)\tDensity(g/cm3)\tVtot(cm3)'
np.savetxt(os.path.join(folder, file.split('.')[0] + '_results.txt'), Out_array, header=header)