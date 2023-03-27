# shrinks tiles one zoom level at a time (used for generating lower zoom levels of river overlay)

import os
import cv2
import numpy as np

least_zoom = int(input("Least zoom: "))

if not os.path.exists(f"..\\data\\river_overlay\\{least_zoom - 1}"):
	os.makedirs(f"..\\data\\river_overlay\\{least_zoom - 1}")

finished_coords = []

for x_coord in os.listdir(f"..\\data\\river_overlay\\{least_zoom}"):
	for y_coord in os.listdir(f"..\\data\\river_overlay\\{least_zoom}\\{x_coord}"):
		if (int(x_coord), int(y_coord.rstrip(".png"))) in finished_coords:
			continue

		needed_coords = []
		for i in range((int(x_coord) // 2) * 2, (int(x_coord) // 2) * 2 + 2):
			for j in range((int(y_coord.rstrip(".png")) // 2) * 2, (int(y_coord.rstrip(".png")) // 2) * 2 + 2):
				needed_coords.append([i, j])

		needed_coords.sort(key=lambda x: x[0])
		needed_coords[:2].sort(key=lambda x: x[1])
		needed_coords[2:].sort(key=lambda x: x[1])

		needed_imgs = []

		for coordinate in needed_coords:
			if os.path.exists(f"..\\data\\river_overlay\\{least_zoom}\\{coordinate[0]}\\{coordinate[1]}.png"):
				needed_imgs.append(cv2.imread(f"..\\data\\river_overlay\\{least_zoom}\\{coordinate[0]}\\{coordinate[1]}.png", cv2.IMREAD_UNCHANGED))
			else:
				needed_imgs.append(np.zeros((256, 256, 4), dtype=np.uint8))

		temp_img1 = np.concatenate((needed_imgs[0], needed_imgs[1]), axis=0)
		temp_img2 = np.concatenate((needed_imgs[2], needed_imgs[3]), axis=0)
		finished_img = np.concatenate((temp_img1, temp_img2), axis=1)

		finished_img = cv2.resize(finished_img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

		empty = True
		for i in range(finished_img.shape[0]):
			for j in range(finished_img.shape[1]):
				if finished_img[i, j, 3] != 0:
					empty = False
					break
			if not empty:
				break
		if not empty:
			if not os.path.exists(f"..\\data\\river_overlay\\{least_zoom - 1}\\{needed_coords[0][0] // 2}"):
				os.makedirs(f"..\\data\\river_overlay\\{least_zoom - 1}\\{needed_coords[0][0] // 2}")

			cv2.imwrite(f"..\\data\\river_overlay\\{least_zoom - 1}\\{needed_coords[0][0] // 2}\\{needed_coords[0][1] // 2}.png", finished_img, [cv2.IMWRITE_PNG_COMPRESSION, 9])

		for coordinate in needed_coords:
			finished_coords.append(coordinate)
