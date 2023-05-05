import cv2


def rgba2rgb(img_path):
	img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
	img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
	cv2.imwrite(img_path, img)


if __name__ == '__main__':
	rgba2rgb(input('Enter the path to the image: '))
