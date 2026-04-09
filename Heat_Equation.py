import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation




# -----------------------------------------------------------
# Parameters
# -----------------------------------------------------------

# Size of plate in metres
size=(10,10)

# Number of grid points
dimensions = (300,300)

hGridSpacing = 1/dimensions[0]
dh = hGridSpacing * size[0]

vGridSpacing = 1/dimensions[1]
dv = hGridSpacing * size[1]



# Time interval between evaluations
dt = 0.01

# Frames between image update
frameSkip = 1

accuracyV = dt / (dv**2)
accuracyH = dt / (dh**2)
print(f'If either of these are large, panic: {accuracyV, accuracyH} (btw I consider larger than ~10 to be too large)')

scenarioNames = ('(1) Random Temps', 
                 '(2) Random Temps but with additional customisability',
                 '(3) Grid with cooler bar in the centre',
                 '(4) Gaussian heat packet')
nLine = '\n'.join(scenarioNames)
text = f"\n ============================== \n\n Scenarios are:\n \n {nLine} \n \n ============================== \n"
print(text)

selection = int(input('Enter the number of the scenario: '))

plate = np.zeros(dimensions)



# ======================= Scenario 1: Random temps

if selection == 1:
    plate.fill(273)
    tempRange = (273,340)

    # Randomly generate temperatures
    temps = np.random.uniform(tempRange[0], tempRange[1], (dimensions[0]-2, dimensions[1] -2))
    
    # [1:-1, 1:-1] means that all values except the edge values, have the new temps assigned to them
    plate[1:-1, 1:-1] = temps
    print(plate)
    thermalDiffusivity = 0.003
    

# ======================= Scenario 2: Random temps (but more customisable)

if selection == 2:
    edgeTemp = float(input('Edge temp: '))
    plate.fill(edgeTemp)
    minTemp = float(input('Random minimum temp: '))
    maxTemp = float(input('Random maximum temp: '))
    tempRange = (minTemp,maxTemp)

    # Randomly generate temperatures
    temps = np.random.uniform(tempRange[0], tempRange[1], (dimensions[0]-2, dimensions[1] -2))
    
    # [1:-1, 1:-1] means that all values except the edge values, have the new temps assigned to them
    plate[1:-1, 1:-1] = temps
    thermalDiffusivity = float(input('Thermal diffusivity (Ideally a low value ~0.1): '))

# ======================= Scenario 3: Cooler central bar

if selection == 3:
    plate.fill(273)
    tempRange = (273,340)

    # Randomly generate temperatures
    temps = np.random.uniform(tempRange[0], tempRange[1], (dimensions[0]-2, dimensions[1] -2))
    
    # [1:-1, 1:-1] means that all values except the edge values, have the new temps assigned to them
    plate[1:-1, 1:-1] = temps

    # Cooler central horizontal bar

    barTemp = 260

    relativeVSize = 0.2
    halfVPoints = int(dimensions[1] * relativeVSize * 0.5)
    midPoint = dimensions[1] // 2
    
    barTop = midPoint + halfVPoints
    barBottom = midPoint - halfVPoints

    # Set bar temp
    plate[barBottom:barTop, 1:-1] = barTemp
    


    print(plate)
    thermalDiffusivity = 0.003












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
time = 0.0
def update(frame):
    global time
    for i in range(stepsPerFrame):
        tempChange()
        time = time + dt
        print(time)
    img.set_data(plate)
    return [img]

animation = FuncAnimation(fig, update, interval=10, blit=True)
plt.show()


