import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Dimensions of discrete grid
dimensions = (300,300)

dt = 0.00001



# Size of plate in metres
size=(1,1)
thermalDiffusivity = 0.01


hGridSpacing = 1/dimensions[0]
dh = hGridSpacing * size[0]

vGridSpacing = 1/dimensions[1]
dv = hGridSpacing * size[1]

plate = np.zeros(dimensions)
plate.fill(273)
dTempPlate = plate

tempRange = (273, 340)


temps = np.random.uniform(tempRange[0],tempRange[1],(dimensions[0]-2, dimensions[1]-2))
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

# Click handler
fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(1,1,1)

brushRadius = 8

def onclick(event):
    if event.button == 1:
        x = int(np.round(event.xdata, 0))
        y = int(np.round(event.ydata, 0))

        yStart = max(0, y-brushRadius)
        yEnd = min(dimensions[1], y + brushRadius)

        xStart= max(0, x-brushRadius)
        xEnd = min(dimensions[0], x + brushRadius)

        if 0 <= x < dimensions[0] and 0 <= y < dimensions[1]:
            plate[yStart: yEnd, xStart: xEnd] = tempRange[1]

#print(plate)

np.set_printoptions(precision=3)


fig.canvas.mpl_connect('button_press_event',onclick)


img = ax.imshow(plate, cmap='hot', animated=True)
plt.colorbar(img)

stepsPerFrame = 30
def update(frame):
    for i in range(stepsPerFrame):
        tempChange()
    img.set_data(plate)
    return [img]

animation = FuncAnimation(fig, update, interval=10, blit=True)
plt.show()


