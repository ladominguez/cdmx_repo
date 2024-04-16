import shapefile as shp  # Requires the pyshp package
import matplotlib.pyplot as plt
from pyproj import Proj, transform

zone = 14
sf = shp.Reader("1ra_Red_vial_primaria_acceso_controlado_cdmx_09_23.shp")
proj_string = "+proj=utm +zone={} +ellps=WGS84".format(zone)
proj_utm = Proj(proj_string)

plt.figure()
for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    lon, lat = proj_utm(x, y, inverse=True)
    plt.plot(lon,lat)
plt.show()
