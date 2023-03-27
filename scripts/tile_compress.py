# compress all png files in a directory and subdirectories (used for compressing river tiles)

import os
import cv2


def compress_png(path):
	count = 0
	all_png = []
	for curr_dir in os.walk(path):
		for file in curr_dir[2]:
			# only do this if file is png
			if file.endswith(".png"):
				all_png.append(f"{curr_dir[0]}\\{file}")
	for png in all_png:
		img = cv2.imread(png, cv2.IMREAD_UNCHANGED)
		cv2.imwrite(png, img, [cv2.IMWRITE_PNG_COMPRESSION, 9])
		count += 1
		print(f"Compressed {count} tiles")


if __name__ == "__main__":
	compress_png(input("Directory: "))
