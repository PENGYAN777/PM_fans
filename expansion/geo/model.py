import math
import numpy as np
from numpy import sin, cos, pi, linspace
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

"""
1. plot the nozzle wall and centerline
"""

lwh = 1
# Define the wall points

x = [0, 0.1, 0.1]
y = [0.1, 0.2, 0.4]

# Plot size settings
fig1 = plt.figure(dpi=300)
axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7])  # size of figure

# Create the plot
axes.plot(x, y, 'k-',linewidth = lwh)

# add  hash line along the wall

for i in range(10):
    y_start = 0.2 + i * 0.02
    y_end = y_start + 0.02
    axes.plot([0.08, 0.1], [y_start, y_end], 'k-', linewidth = lwh/2)

for i in range(5):
    x = i * 0.02
    y_start = 0.1 + i * 0.02
    y_end = y_start + 0.02
    axes.plot([x, x], [y_start, y_end], 'k-', linewidth = lwh/2)

# plot centerline 
axes.plot([0,1], [0,0], 'k-', linewidth = lwh)

"""
2. plot the flow features
"""

# constant pressure boundary
angles = linspace(0.4 * pi, 0.7* pi, 100 )
xs = 0.4 + cos(angles)*0.3 
ys = 0.05 +sin(angles)*0.3 
plt.plot(xs, ys, 'k-', linewidth = lwh)

# expand externally

axes.plot([0.1,0.35], [0.2,0.34], 'k--', linewidth = lwh)
axes.plot([0.35,0.5], [0.34,0.2], 'k--', linewidth = lwh)


axes.plot([0.1,0.3], [0.2,0.33], 'k--', linewidth = lwh)
axes.plot([0.3,0.5], [0.33,0.2], 'k--', linewidth = lwh)

# interception and reflected shock, Mach disk

axes.plot([0.5,0.6], [0.2,0.1], 'r', linewidth = lwh)
axes.plot([0.6,0.8], [0.1,0.3], 'r', linewidth = lwh)
axes.plot([0.6,0.6], [0.1,0.0], 'r', linewidth = lwh)


# horizontal line
axes.plot([0.1,0.3], [0.2,0.2], 'k--', linewidth = lwh)

# expand internally
axes.plot([0.1,0.5], [0.2,0.0], 'k--', linewidth = lwh)
axes.plot([0.1,0.6], [0.2,0.0], 'k--', linewidth = lwh)

# Labels
plt.text(0.18, 0.26, '$a$',ha= 'center', size =8)
plt.text(0.18, 0.22, '$b$',ha= 'center', size =8)

plt.text(0.18, 0.17, '$c$',ha= 'center', size =8)
plt.text(0.18, 0.13, '$d$',ha= 'center', size =8)

plt.text(0.35, 0.36, 'Contact surface',ha= 'center', size =6)
plt.text(0.43, 0.15, 'Interception shock',ha= 'center', size =6)
plt.text(0.76, 0.15, 'Reflected shock',ha= 'center', size =6)
plt.text(0.67, 0.05, 'Mach disk',ha= 'center', size =6)



# Set aspect ratio to 'equal' and box
axes.set_aspect('equal', 'box')

# Turn off the axes
plt.axis('off')

# Save the figure as a .eps file
fig1.savefig("geo_model.png")
