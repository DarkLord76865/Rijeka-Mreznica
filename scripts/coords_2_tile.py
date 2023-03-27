# Convert coordinates to tile number for every zoom level

import math

# zoom = int(input("Zoom: "))
lat_deg, lon_deg = map(float, input("Coordinates: ").split())
lat_rad = math.radians(lat_deg)


for zoom in range(0, 22):

	n = 2 ** zoom
	xtile = n * ((lon_deg + 180) / 360)
	ytile = n * (1 - (math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)) / 2

	print(f"Zoom {zoom}: ", int(math.floor(xtile)), int(math.floor(ytile)))
