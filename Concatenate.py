import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
import os

application_window = tk.Tk()
wd = filedialog.askdirectory(title='Select day directory', parent=application_window)
application_window.destroy()

Depth = np.array([])
Density = np.array([])
Vop = np.array([])
Vcl = np.array([])
Vtot = np.array([])

for f in os.listdir(wd):
    filename = os.path.join(wd, f)
    Data = np.loadtxt(filename)
    Depth = np.append(Depth, Data[:,0])
    Density = np.append(Density, Data[:,-2])
    Vop = np.append(Vop, Data[:,1])
    Vcl = np.append(Vcl, Data[:,3])
    Vtot = np.append(Vtot, Data[:, -1])

# ----------- PLOT ------------

# Plot Open and Closed porosity VS Depth
fig = plt.figure(figsize=(14,6))
fig.subplots_adjust(top=.95,bottom=.1,left=.05,right=.95)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax1.scatter(Depth, Vop/Vtot, s=100, marker='o', edgecolor='#050505')
ax2.scatter(Depth, Vcl/Vtot, s=100,  marker='s', c='orange', edgecolor='#050505')
ax1.set_ylabel('Open Porosity')
ax2.set_ylabel('Closed Porosity')
ax1.set_xlabel('Depth (m)')
# ax1.grid(True)
plt.show()

# Plot Closed/Total porosity VS Depth
fig = plt.figure(figsize=(14,6))
fig.subplots_adjust(top=.95,bottom=.1,left=.05,right=.95)
ax1 = fig.add_subplot(111)
ax1.scatter(Depth, Vcl/(Vop+Vcl), s=100, marker='o', cmap='viridis', edgecolor='#050505')
ax1.set_ylabel('Closed/Total Porosity')
ax1.set_xlabel('Depthy (m)')
# ax1.grid(True)
plt.show()

# Plot Open and Closed porosity VS Density
fig = plt.figure(figsize=(14,6))
fig.subplots_adjust(top=.95,bottom=.1,left=.05,right=1.00)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
sc = ax1.scatter(Density, Vop/Vtot, s=100, c=Depth, marker='o', cmap='viridis', edgecolor='#050505')
ax2.scatter(Density, Vcl/Vtot, s=100, c=Depth, marker='s', cmap='viridis', edgecolor='#050505')
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
sc = ax1.scatter(Density, Vcl/(Vcl+Vop), s=100, c=Depth, marker='o', cmap='viridis', edgecolor='#050505')
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
sc = ax1.scatter((Vop+Vcl)/Vtot, Vcl/Vtot, s=100, c=Depth, marker='o', cmap='viridis', edgecolor='#050505')
cax = fig.colorbar(sc)
cax.set_label('Depth (m)')
ax1.set_ylabel('Closed Porosity')
ax1.set_xlabel('Total Porosity')
# ax1.grid(True)
plt.show()

# Save data
# header = 'Depth\tVop(cm3)\tdVop(cm3)\tVcl(cm3)\tdVcl(cm3)\tDensity(g/cm3)'
# np.savetxt(os.path.join(folder, file.split('.')[0] + '_results.txt'), Out_array, header=header)