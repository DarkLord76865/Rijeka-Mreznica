# removes data about pixels that are transparent (alpha = 0) (saves space)

import os
import cv2


def clean_imgs(path):
	count = 0
	all_png = []
	for curr_dir in os.walk(path):
		for file in curr_dir[2]:
			# only do this if file is png
			if file.endswith(".png"):
				all_png.append(f"{curr_dir[0]}\\{file}")
	for png in all_png:
		img = cv2.imread(png, cv2.IMREAD_UNCHANGED)
		for row in img:
			for pixel in row:
				if pixel[3] == 0:
					pixel[0] = 0
					pixel[1] = 0
					pixel[2] = 0
		cv2.imwrite(png, img)
		count += 1
		print(f"Cleaned {count} tiles")


if __name__ == "__main__":
	clean_imgs(input("Directory: "))
