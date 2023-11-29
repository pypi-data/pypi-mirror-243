import fsc
from fsc.devices import w7x
fsc.resolve.importOfflineData("w7x.fsc")
grid = w7x.defaultGrid.clone()
grid.nR = 128
grid.nZ = 128
grid.nPhi = 32

print(grid)

geoGrid = w7x.defaultGeometryGrid.clone()
print(geoGrid)
tracer = fsc.tracer()

cadCoils = w7x.computeCoilFields(tracer.calculator, w7x.cadCoils(), grid = grid)
fsc.data.writeArchive(cadCoils, "cadCoils.fsc")

print("Done, exiting")