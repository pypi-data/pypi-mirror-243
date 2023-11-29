import fusionsc as fsc
import numpy as np
import pyvista as pv

from fusionsc.devices import w7x

fsc.resolve.importOfflineData("w7x-op21.fsc")

i12345 = [15000] * 5
iab = [0] * 2

# Compute magnetic field
print("Computing field")
config = w7x.mainField(i12345, iab).compute(w7x.defaultGrid())
print("Done")

phi = 0
rStart = 6
zStart = 0

xStart = np.cos(phi) * rStart
yStart = np.sin(phi) * rStart

pStart = np.asarray([xStart, yStart, zStart])

print("Tracing 1")
fieldLineFwd, fieldStrengthFwd = fsc.flt.followFieldlines(pStart, config, direction = "ccw", distanceLimit = 7 * np.radians(72))
print("Tracing 2")
fieldLineBwd, fieldStrengthBwd = fsc.flt.followFieldlines(pStart, config, direction = "cw", distanceLimit = 7 * np.radians(72))

def plotResult(xyz, b):
	x, y, z = xyz
	phi = np.arctan2(y, x)
	plt.plot(np.degrees(phi), b)

import matplotlib.pyplot as plt

plt.figure()
plotResult(fieldLineFwd, fieldStrengthFwd)
plotResult(fieldLineBwd, fieldStrengthBwd)
plt.xlabel("Phi [deg]")
plt.ylabel("B [T]")
plt.show()
