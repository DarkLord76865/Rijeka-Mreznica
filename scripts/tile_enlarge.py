# enlarges tiles for all missing zoom levels up to a maximum zoom level (used for generating bigger zoom levels for the river overlay)

import os
import cv2
import numpy as np


base_zoom = int(input("Base zoom: "))
max_zoom = int(input("Max zoom: "))

kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])

blur_kernel = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]]) / 9

for zoom in range(base_zoom + 1, max_zoom):
	if not os.path.exists(f"..\\data\\river_overlay\\{zoom + 1}"):
		os.makedirs(f"..\\data\\river_overlay\\{zoom + 1}")

for x_coord in os.listdir(f"..\\data\\river_overlay\\{base_zoom}"):
	for y_coord in os.listdir(f"..\\data\\river_overlay\\{base_zoom}\\{x_coord}"):

		file_name = f"..\\data\\river_overlay\\{base_zoom}\\{x_coord}\\{y_coord}"
		base_img = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)

		base_img = cv2.filter2D(src=base_img, ddepth=-1, kernel=blur_kernel)
		base_img = cv2.filter2D(src=base_img, ddepth=-1, kernel=blur_kernel)
		base_img = cv2.filter2D(src=base_img, ddepth=-1, kernel=kernel)

		for zoom in range(1, max_zoom - base_zoom + 1):
			curr_img = cv2.resize(base_img, None, fx=(2 ** zoom), fy=(2 ** zoom), interpolation=cv2.INTER_CUBIC)

			separated_images = []
			separated_images_coords = []

			for i in range(2 ** zoom):
				for j in range(2 ** zoom):
					separated_images.append(curr_img[i * 256:(i + 1) * 256, j * 256:(j + 1) * 256])
					separated_images_coords.append((int(x_coord) * (2 ** zoom) + j, int(y_coord.rstrip(".png")) * (2 ** zoom) + i))

			for ind in range(len(separated_images)):
				empty = True
				for i in range(256):
					for j in range(256):
						if separated_images[ind][i, j, 3] != 0:
							empty = False
							break
					if not empty:
						break

				if not empty:
					if not os.path.exists(f"..\\data\\river_overlay\\{base_zoom + zoom}\\{separated_images_coords[ind][0]}"):
						os.makedirs(f"..\\data\\river_overlay\\{base_zoom + zoom}\\{separated_images_coords[ind][0]}")

					cv2.imwrite(f"..\\data\\river_overlay\\{base_zoom + zoom}\\{separated_images_coords[ind][0]}\\{separated_images_coords[ind][1]}.png", separated_images[ind])
