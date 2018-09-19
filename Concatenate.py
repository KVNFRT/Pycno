import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from tkinter import filedialog
import tkinter as tk
import os

application_window = tk.Tk()
wd = filedialog.askdirectory(title='Select day directory', parent=application_window)
application_window.destroy()

header = 'Depth\tVop(cm3)\tdVop(cm3)\tVcl(cm3)\tdVcl(cm3)\tCR\tdCR\tVptot(cm3)\tVcyl(cm3)\tDensity(g/cm3)\tRelative_Density'
Depth = np.array([])
Vop = np.array([])
dVop = np.array([])
Vcl = np.array([])
dVcl = np.array([])
CR = np.array([])
dCR = np.array([])
Vpt = np.array([])
Vcyl = np.array([])
Density = np.array([])
RDensity = np.array([])

for f in os.listdir(wd):
    filename = os.path.join(wd, f)
    Data = np.loadtxt(filename)
    Depth = np.append(Depth, Data[:,0])       # Depth
    Vop = np.append(Vop, Data[:, 1])  # Open porosity volume (cm3)
    dVop = np.append(dVop, Data[:, 2])  # Open porosity volume (cm3)
    Vcl = np.append(Vcl, Data[:,3])           # Closed porosity volume (cm3)
    dVcl = np.append(dVcl, Data[:,4])           # Closed porosity volume (cm3)
    CR = np.append(Vcl, Data[:,5])           # Closed porosity volume (cm3)
    dCR = np.append(dVcl, Data[:,6])           # Closed porosity volume (cm3)
    Vpt = np.append(Vpt, Data[:, 7])         # Total porosity volume (cm3)
    Vcyl = np.append(Vcyl, Data[:, 8])         # Total porosity volume (cm3)
    Density = np.append(Density, Data[:,9])  # Density
    RDensity = np.append(RDensity, Data[:,10])  # Density


# ----------- PLOT ------------

# Plot Open and Closed porosity VS Depth
fig = plt.figure(figsize=(14,6))
fig.subplots_adjust(top=.95,bottom=.1,left=.05,right=.95)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax1.scatter(Depth, Vop/Vcyl, s=100, marker='o', edgecolor='#050505')
ax2.scatter(Depth, Vcl/Vcyl, s=100,  marker='s', c='orange', edgecolor='#050505')
ax1.set_ylabel('Open Porosity')
ax2.set_ylabel('Closed Porosity')
ax1.set_xlabel('Depth (m)')
# ax1.grid(True)
plt.show()

# Plot Closed/Total porosity VS Depth
fig = plt.figure(figsize=(14,6))
fig.subplots_adjust(top=.95,bottom=.1,left=.05,right=.95)
ax1 = fig.add_subplot(111)
ax1.scatter(Depth, CR, s=100, marker='o', cmap='viridis', edgecolor='#050505')
ax1.set_ylabel('Closed/Total Porosity')
ax1.set_xlabel('Depth (m)')
# ax1.grid(True)
plt.show()

# Plot Open and Closed porosity VS Density
fig = plt.figure(figsize=(14,6))
fig.subplots_adjust(top=.95,bottom=.1,left=.05,right=1.00)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
cmap = cm.get_cmap('viridis', 20)
sc = ax1.scatter(Density, Vop/Vpt, s=100, c=Depth, marker='o', cmap=cmap, edgecolor='#050505')
ax2.scatter(Density, Vcl/Vpt, s=100, c=Depth, marker='s', cmap=cmap, edgecolor='#050505')
cax = fig.colorbar(sc)
cax.set_label('Depth (m)')
ax1.set_ylabel('Open Porosity')
ax2.set_ylabel('Closed Porosity')
ax1.set_xlabel('Density (g/cm3)')
# ax1.grid(True)
plt.show()

# Plot Closed/Total porosity VS Density
fig = plt.figure(figsize=(14,6))
fig.subplots_adjust(top=.95,bottom=.1,left=.05,right=1.00)
ax1 = fig.add_subplot(111)
cmap = cm.get_cmap('viridis', 20)
sc = ax1.scatter(Density, CR, s=100, c=Depth, marker='o', cmap=cmap, edgecolor='#050505')
cax = fig.colorbar(sc)
cax.set_label('Depth (m)')
ax1.set_ylabel('Closed/Total Porosity' )
ax1.set_xlabel('Density (g/cm3)')
# ax1.grid(True)
plt.show()

# Plot Closed/Total porosity VS Density
fig = plt.figure(figsize=(14,6))
fig.subplots_adjust(top=.95,bottom=.1,left=.05,right=1.00)
ax1 = fig.add_subplot(111)
cmap = cm.get_cmap('viridis', 20)
sc = ax1.scatter(Vpt/Vcyl, Vcl/Vcyl, s=100, c=Depth, marker='o', cmap=cmap, edgecolor='#050505')
ax1.plot([0,.2],[0,.2], ls='--', c='#0A0A0A')
cax = fig.colorbar(sc)
cax.set_label('Depth (m)')
ax1.set_ylabel('Closed Porosity')
ax1.set_xlabel('Total Porosity')
# ax1.grid(True)
plt.show()

# Plot Closed/Total porosity VS Density
fig = plt.figure(figsize=(14,6))
fig.subplots_adjust(top=.95,bottom=.1,left=.05,right=1.00)
ax1 = fig.add_subplot(111)
cmap = cm.get_cmap('viridis', 20)
sc = ax1.scatter(Vpt/Vcyl, Vcl/Vcyl, s=100, c=Density, marker='o', cmap=cmap, edgecolor='#050505')
#ax1.scatter((Vcl+Vop)/Vtot, Vclraw/Vtot, s=100, marker='o', edgecolor='#050505')
ax1.plot([0,.2],[0,.2], ls='--', c='#0A0A0A')
cax = fig.colorbar(sc)
cax.set_label('Density (g/cm3)')
ax1.set_ylabel('Closed Porosity')
ax1.set_xlabel('Total Porosity')
# ax1.grid(True)
plt.show()

# Save data
header = 'Depth\tVop(cm3)\tdVop(cm3)\tVcl(cm3)\tdVcl(cm3)\tCR\tdCR\tVptot(cm3)\tVcyl(cm3)\tDensity(g/cm3)\tRelative_Density'
np.savetxt(os.path.join(wd, os.path.pardir, 'Closed_porosity.txt'), np.column_stack((Depth , Vop, dVop, Vcl, dVcl, CR, dCR, Vpt, Vcyl, Density, RDensity)), header=header)