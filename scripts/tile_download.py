# download tiles from a tile server (used downloading base map tiles while creating the river overlay)

import os
import requests
import shutil


tile_server = "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
last_zoom = int(input("Enter the last zoom level: "))

if os.path.exists(f"..\\data\\river_overlay\\{last_zoom}"):
	for x_coord in os.listdir(f"..\\data\\river_overlay\\{last_zoom}"):
		x_coords = [int(x_coord.rstrip(".png")) * 2, int(x_coord.rstrip(".png")) * 2 + 1]
		y_coords = []
		for y_coord in os.listdir(f"..\\data\\river_overlay\\{last_zoom}\\{x_coord}"):
			y_coords.extend((int(y_coord.rstrip(".png")) * 2, int(y_coord.rstrip(".png")) * 2 + 1))

		for x in x_coords:
			for y in y_coords:
				url = tile_server.format(z=last_zoom + 1, x=x, y=y)
				file_name = f"..\\data\\river_overlay\\{last_zoom + 1}\\{x}\\{y}.png"

				if not os.path.exists(os.path.dirname(file_name)):
					os.makedirs(os.path.dirname(file_name))

				res = requests.get(url, stream=True, headers={"User-Agent": "TkinterMapView"})

				if res.status_code == 200:
					with open(file_name, 'wb') as f:
						shutil.copyfileobj(res.raw, f)
				else:
					raise Exception(f"Error downloading file: {url}")
