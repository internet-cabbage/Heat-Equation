import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Dimensions of discrete grid
dimensions = (300,300)

dt = 0.001



# Size of plate in metres
size=(1,1)
thermalDiffusivity = 0.001


hGridSpacing = 1/dimensions[0]
dh = hGridSpacing * size[0]

vGridSpacing = 1/dimensions[1]
dv = hGridSpacing * size[1]

plate = np.zeros(dimensions)
plate.fill(273)
dTempPlate = plate


temps = np.random.uniform(273,300,(dimensions[0]-2, dimensions[1]-2))
plate[1:-1, 1:-1] = temps

def tempChange():

    # X and Y are swapped (Y,X)
    centre = plate[1:-1, 1:-1]
    left = plate[1:-1, :-2]
    right = plate[1:-1, 2:]
    upper = plate[:-2, 1:-1]
    lower = plate[2:, 1:-1]

    tempDDotHor = (right + left - 2 * centre ) / (dh**2)
    tempDDotVert = (upper + lower - 2 * centre) / (dv**2)

    dTemp = thermalDiffusivity * (tempDDotVert + tempDDotHor) * dt
    plate[1:-1, 1:-1] = plate[1:-1, 1:-1] + dTemp

print(plate)

np.set_printoptions(precision=3)

fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(1,1,1)

img = ax.imshow(plate, cmap='hot', animated=True)
plt.colorbar(img)


def update(frame):
    tempChange()
    img.set_data(plate)
    return [img]

animation = FuncAnimation(fig, update, interval=100, blit=True)
plt.show()



