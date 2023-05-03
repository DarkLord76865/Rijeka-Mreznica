import json
import os
import sys
import tkinter
import tkinter.font as tkinterfont

import cv2
import numpy as np
import tkintermapview
from PIL import Image as ImagePIL
from PIL import ImageTk


class Background:
	def __init__(self, root, relx, rely, relwidth, relheight):
		self.root = root
		self.relx = relx
		self.rely = rely
		self.relwidth = relwidth
		self.relheight = relheight

		self.wood_texture = cv2.cvtColor(cv2.imread(resource_path("data\\wood_texture.png"), cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGB)

		self.widget = tkinter.Canvas(self.root, borderwidth=0, highlightthickness=0)

		self.img = self.widget.create_image(0, 0, anchor="nw")
		self.img_data = None

		self.title = self.widget.create_text(10, 10, anchor=tkinter.CENTER, text="Rijeka Mrežnica", fill="#ffffff")
		self.title_font = tkinterfont.Font(family="Arial", size=25, weight="bold")

		self.widget.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=self.relheight)

		self.update()

	def update(self):
		self.widget.update()
		self.update_img(self.widget.winfo_width(), self.widget.winfo_height())

		font_height = self.title_font.metrics("ascent") + self.title_font.metrics("descent")
		if font_height > self.widget.winfo_height() * 0.20:
			while font_height > self.widget.winfo_height() * 0.20:
				self.title_font.configure(size=self.title_font["size"] - 1)
				font_height = self.title_font.metrics("ascent") + self.title_font.metrics("descent")
		else:
			while font_height < self.widget.winfo_height() * 0.20:
				self.title_font.configure(size=self.title_font["size"] + 1)
				font_height = self.title_font.metrics("ascent") + self.title_font.metrics("descent")
			self.title_font.configure(size=self.title_font["size"] - 1)
			font_height = self.title_font.metrics("ascent") + self.title_font.metrics("descent")

		font_length = self.title_font.measure("Rijeka Mrežnica")
		while font_length > self.widget.winfo_width() * 0.90:
			self.title_font.configure(size=self.title_font["size"] - 1)
			font_length = self.title_font.measure("Rijeka Mrežnica")

		self.widget.itemconfig(self.title, font=self.title_font)
		self.widget.coords(self.title, self.widget.winfo_width() // 2, (self.widget.winfo_height() * 0.20) // 2)

	def update_img(self, width, height):
		background_image = self.wood_texture

		while background_image.shape[0] < height:
			background_image = np.concatenate((background_image, self.wood_texture), axis=0)

		while background_image.shape[1] < width:
			background_image = np.concatenate((background_image, background_image), axis=1)

		background_image = background_image[:height, :width]

		self.img_data = ImageTk.PhotoImage(ImagePIL.fromarray(background_image))
		self.widget.itemconfig(self.img, image=self.img_data)

class Map:
	def __init__(self, root, relx, rely, relwidth, relheight, max_zoom=19, map_server="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", overlay_server="", zoom=10, center=(45.295, 15.44)):
		self.root = root

		self.relx = relx
		self.rely = rely
		self.relwidth = relwidth
		self.relheight = relheight

		self.max_zoom = max_zoom
		self.map_server = map_server
		self.overlay_server = overlay_server

		self.zoom = zoom
		self.center = center

		self.widget = tkintermapview.TkinterMapView(self.root, borderwidth=0, highlightthickness=0)
		self.widget.set_zoom(self.zoom)
		self.widget.set_position(*self.center)

		self.widget.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=self.relheight)

		self.update()

	def change_map(self, map_server):
		self.map_server = map_server
		self.update()

	def change_overlay(self, overlay_server):
		self.overlay_server = overlay_server
		self.update()

	def update(self):
		self.widget.set_tile_server(self.map_server)
		self.widget.set_overlay_tile_server(self.overlay_server)

	def center_map(self):
		self.widget.set_position(*self.center)
		self.widget.set_zoom(self.zoom)


def load_json(file_path):

	with open(file_path, "r", encoding="utf-8") as file:
		info = json.load(file)

	return info

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def resize(event):
	global background_object
	global width, height

	if event.widget != root or (event.width == width and event.height == height):
		return

	width = event.width
	height = event.height

	background_object.update()


# create tkinter window
root = tkinter.Tk()
width = 1024
height = 576
root.geometry(f"{width}x{height}+{(root.winfo_screenwidth() // 2) - (width // 2)}+{(root.winfo_screenheight() // 2) - (height // 2)}")
root.minsize(width, height)
root.title("Rijeka Mrežnica")
root.iconbitmap(resource_path("data\\river-icon.ico"))
root.bind("<Configure>", resize)

MAP_SERVERS = {
	"OpenStreetMap": "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
	"Google-map": "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
	"Google-satellite": "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
}

MREZNICA_DATA = load_json(resource_path("data\\mreznica.json"))

MARKERS = dict()
for file in os.listdir(resource_path("data\\map_markers")):
	if file.endswith(".png"):
		MARKERS[file[4:-4]] = ImageTk.PhotoImage(file=resource_path(f"data\\map_markers\\{file}"))

background_object = Background(root, relx=0.5, rely=0.0, relwidth=0.5, relheight=1.0)
map_object = Map(root, relx=0.0, rely=0.0, relwidth=0.5, relheight=1.0, max_zoom=19, map_server=MAP_SERVERS["Google-satellite"], overlay_server="file://data/river_overlay/{z}/{x}/{y}.png", zoom=10, center=(45.295, 15.44))

crosshair_img_grey = ImageTk.PhotoImage(file=resource_path(f"data\\crosshair-grey.png"))
crosshair_img_lightgrey = ImageTk.PhotoImage(file=resource_path(f"data\\crosshair-lightgrey.png"))
center_button = tkinter.Label(root, image=crosshair_img_grey, bg="white", borderwidth=0, highlightthickness=0, cursor="hand2")
center_button.bind("<Button-1>", lambda event: map_object.center_map())
center_button.bind("<Enter>", lambda event: center_button.config(image=crosshair_img_lightgrey))
center_button.bind("<Leave>", lambda event: center_button.config(image=crosshair_img_grey))
center_button.place(x=20, y=100, width=30, height=30)

"""
marker = map_widget.set_marker(45.5981525, 15.7563562, "test", icon=icon1, icon_anchor="s")
#marker.change_icon(icon)
#marker.command = testt

marker2 = map_widget.set_marker(45.0, 45.001, "test")
# marker2.image = img
marker2.image_zoom_visibility = (10, float("inf"))
marker2.icon = icon2
"""

root.mainloop()
