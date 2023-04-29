import tkinter
import tkintermapview
from PIL import ImageTk
from PIL import Image as ImagePIL
import os
import sys
import cv2
import numpy as np


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def create_background_image(width, height):
	global wood_texture

	background_image = wood_texture.copy()

	while background_image.shape[0] < height:
		background_image = np.concatenate((background_image, wood_texture), axis=0)

	while background_image.shape[1] < width:
		background_image = np.concatenate((background_image, background_image), axis=1)

	background_image = background_image[:height, :width]

	return background_image

def resize(event):
	global width
	global height
	global root

	global background_img
	global background_lbl

	if event.widget != root or (event.width == width and event.height == height):
		return

	width = event.width
	height = event.height

	background_img = ImageTk.PhotoImage(ImagePIL.fromarray(create_background_image(width, height)))
	background_lbl.config(image=background_img)


MAP_SERVERS = {
	"OpenStreetMap": "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
	"Google-map": "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
	"Google-satellite": "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
}

wood_texture = cv2.cvtColor(cv2.imread(resource_path("data\\wood_texture.png"), cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGB)

# create tkinter window
root = tkinter.Tk()
width = 650
height = 500
root.geometry(f"{width}x{height}+{(root.winfo_screenwidth() // 2) - (width // 2)}+{(root.winfo_screenheight() // 2) - (height // 2)}")
root.minsize(width, height)
root.title("Rijeka Mrežnica")
root.iconbitmap(resource_path("data\\river-icon.ico"))

root.bind("<Configure>", resize)

background_img = ImageTk.PhotoImage(ImagePIL.fromarray(create_background_image(width, height)))
background_lbl = tkinter.Label(root, image=background_img, borderwidth=0, highlightthickness=0)
background_lbl.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
# create map widget

map_widget = tkintermapview.TkinterMapView(root, borderwidth=0, highlightthickness=0)
map_widget.place(relwidth=0.5, relheight=1.0, rely=0.0, relx=0.0)
map_widget.set_tile_server(MAP_SERVERS["Google-map"], max_zoom=19)
map_widget.set_overlay_tile_server("file://{file_path}".format(file_path=resource_path("data\\river_overlay\\{z}\\{x}\\{y}.png")))
map_widget.set_zoom(10)
map_widget.set_position(45.295, 15.44)


icon1 = ImageTk.PhotoImage(file="data\\map_markers\\mark1.png")
icon2 = ImageTk.PhotoImage(file="data\\map_markers\\mark2.png")
marker = map_widget.set_marker(45.5981525, 15.7563562, "test", icon=icon1, icon_anchor="s")
#marker.change_icon(icon)
#marker.command = testt

marker2 = map_widget.set_marker(45.0, 45.001, "test")
# marker2.image = img
marker2.image_zoom_visibility = (10, float("inf"))
marker2.icon = icon2


root.mainloop()
