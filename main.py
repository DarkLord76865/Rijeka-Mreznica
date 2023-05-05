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


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def load_json(file_path):
	""" Load json file """
	with open(file_path, "r", encoding="utf-8") as file:
		info = json.load(file)

	return info


class Background:
	def __init__(self, root, relx, rely, relwidth, relheight):
		self.root = root
		self.relx = relx
		self.rely = rely
		self.relwidth = relwidth
		self.relheight = relheight

		self.wood_texture = cv2.cvtColor(cv2.imread(resource_path("data\\wood_texture.png"), cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGB)

		self.widget = tkinter.Canvas(self.root, borderwidth=0, highlightthickness=0)
		self.widget.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=self.relheight)
		self.widget.update()

		self.bg = self.widget.create_image(0, 0, anchor="nw")
		self.bg_data = None

		self.title = self.widget.create_text(10, 10, anchor=tkinter.CENTER, text="Mrežnica", fill="#ffffff")
		self.title_font = tkinterfont.Font(family="Gabriola", size=25, weight="bold")

		self.img_frame = Image(self.widget, 0.5, 0.5, 0.9, 0.4)

		self.update()

		self.width = self.widget.winfo_width()
		self.height = self.widget.winfo_height()

		self.widget.bind("<Configure>", self.resize)

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

		font_length = self.title_font.measure("Rijeka Mrežnica")
		while font_length > self.widget.winfo_width() * 0.90:
			self.title_font.configure(size=self.title_font["size"] - 1)
			font_length = self.title_font.measure("Rijeka Mrežnica")

		self.widget.itemconfig(self.title, font=self.title_font)
		self.widget.coords(self.title, self.widget.winfo_width() // 2, (self.widget.winfo_height() * 0.20) // 2)

		self.img_frame.update()

	def update_img(self, width, height):
		background_image = self.wood_texture

		while background_image.shape[0] < height:
			background_image = np.concatenate((background_image, self.wood_texture), axis=0)

		while background_image.shape[1] < width:
			background_image = np.concatenate((background_image, background_image), axis=1)

		background_image = background_image[:height, :width]

		self.bg_data = ImageTk.PhotoImage(ImagePIL.fromarray(background_image))
		self.widget.itemconfig(self.bg, image=self.bg_data)

	def resize(self, event):
		if event.widget == self.widget and (event.width != self.width or event.height != self.height):
			self.width = event.width
			self.height = event.height
			self.update()

class Map:
	def __init__(self, root, relx, rely, relwidth, relheight, max_zoom=19, map_server="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", overlay_server="", zoom=10, center=(45.295, 15.46)):
		self.root = root

		self.MARKERS = dict()
		for file in os.listdir(resource_path("data\\map_markers")):
			if file.endswith(".png"):
				self.MARKERS[file[4:-4]] = ImageTk.PhotoImage(file=resource_path(f"data\\map_markers\\{file}"))

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

class Image:
	def __init__(self, master, relx, rely, relwidth, relheight):
		self.master = master
		self.master_width = self.master.winfo_width()
		self.master_height = self.master.winfo_height()

		self.relx = relx
		self.rely = rely
		self.relwidth = relwidth
		self.relheight = relheight

		self.x = int(round(relx * self.master_width, 0))
		self.y = int(round(rely * self.master_height, 0))
		self.width = int(round(relwidth * self.master_width, 0))
		self.height = int(round(relheight * self.master_height, 0))

		self.is_blank = True
		self.blank_image = cv2.imread(resource_path("data\\no-image.png"), cv2.IMREAD_UNCHANGED)

		self.frame_data = ImageTk.PhotoImage(ImagePIL.fromarray(self.generate_blank()))
		self.frame = self.master.create_image(self.x, self.y, anchor="center", image=self.frame_data)

	def update(self):
		self.master_width = self.master.winfo_width()
		self.master_height = self.master.winfo_height()
		self.x = int(round(self.relx * self.master_width, 0))
		self.y = int(round(self.rely * self.master_height, 0))
		self.width = int(round(self.relwidth * self.master_width, 0))
		self.height = int(round(self.relheight * self.master_height, 0))
		self.master.coords(self.frame, self.x, self.y)
		if self.is_blank:
			self.frame_data = ImageTk.PhotoImage(ImagePIL.fromarray(self.generate_blank()))
			self.master.itemconfig(self.frame, image=self.frame_data)

	def generate_blank(self):
		img = np.full((self.height, self.width, 3), 51, dtype=np.uint8)
		y_low = int(round(img.shape[0] / 2 - self.blank_image.shape[0] / 2, 0))
		y_high = y_low + self.blank_image.shape[0]
		x_low = int(round(img.shape[1] / 2 - self.blank_image.shape[1] / 2, 0))
		x_high = x_low + self.blank_image.shape[1]
		img[y_low:y_high, x_low:x_high] = self.blank_image

		return img

class App:
	def __init__(self, root):
		self.root = root
		self.root.title("Rijeka Mrežnica")
		self.root.iconbitmap(resource_path("data\\river-icon.ico"))
		self.width = 960
		self.height = 720
		self.root.geometry(f"{self.width}x{self.height}+{(self.root.winfo_screenwidth() // 2) - (self.width // 2)}+{(self.root.winfo_screenheight() // 2) - (self.height // 2)}")
		self.root.minsize(self.width, self.height)
		self.root.bind("<Configure>", self.resize)

		self.background = Background(self.root, relx=0.5, rely=0.0, relwidth=0.5, relheight=1.0)

		self.map_server = "Google-satellite"
		self.overlay_active = True
		self.map = Map(self.root, relx=0.0, rely=0.0, relwidth=0.5, relheight=1.0, map_server=MAP_SERVERS[self.map_server], overlay_server=OVERLAY_SERVER if self.overlay_active else "", zoom=10, center=(45.295, 15.46))
		self.root.after(100, self.map.center_map)

		self.center_btn_img_grey = ImageTk.PhotoImage(file=resource_path(f"data\\crosshair-grey.png"))
		self.center_btn_img_lightgrey = ImageTk.PhotoImage(file=resource_path(f"data\\crosshair-lightgrey.png"))
		self.center_btn = tkinter.Label(self.root, image=self.center_btn_img_grey, borderwidth=0, highlightthickness=0, cursor="hand2")
		self.center_btn.bind("<Button-1>", lambda event: self.map.center_map())
		self.center_btn.bind("<Enter>", lambda event: self.center_btn.config(image=self.center_btn_img_lightgrey))
		self.center_btn.bind("<Leave>", lambda event: self.center_btn.config(image=self.center_btn_img_grey))
		self.center_btn.place(x=20, y=120, width=30, height=30)

		self.osm_btn_img_grey = ImageTk.PhotoImage(file=resource_path(f"data\\osm-grey.png"))
		self.osm_btn_img_lightgrey = ImageTk.PhotoImage(file=resource_path(f"data\\osm-lightgrey.png"))
		self.osm_btn = tkinter.Label(self.root, image=self.osm_btn_img_grey if self.map_server != "OpenStreetMap" else self.osm_btn_img_lightgrey, borderwidth=0, highlightthickness=0, cursor="hand2")
		self.osm_btn.bind("<Button-1>", lambda event: self.map_change(self.osm_btn, "OpenStreetMap"))
		self.osm_btn.bind("<Enter>", lambda event: self.map_change_hover(self.osm_btn, "OpenStreetMap", self.osm_btn_img_lightgrey))
		self.osm_btn.bind("<Leave>", lambda event: self.map_change_hover(self.osm_btn, "OpenStreetMap", self.osm_btn_img_grey))
		self.osm_btn.place(x=20, y=self.height - 120, width=30, height=30)

		self.google_map_btn_img_grey = ImageTk.PhotoImage(file=resource_path(f"data\\google-map-grey.png"))
		self.google_map_btn_img_lightgrey = ImageTk.PhotoImage(file=resource_path(f"data\\google-map-lightgrey.png"))
		self.google_map_btn = tkinter.Label(self.root, image=self.google_map_btn_img_grey if self.map_server != "Google-map" else self.google_map_btn_img_lightgrey, borderwidth=0, highlightthickness=0, cursor="hand2")
		self.google_map_btn.bind("<Button-1>", lambda event: self.map_change(self.google_map_btn, "Google-map"))
		self.google_map_btn.bind("<Enter>", lambda event: self.map_change_hover(self.google_map_btn, "Google-map", self.google_map_btn_img_lightgrey))
		self.google_map_btn.bind("<Leave>", lambda event: self.map_change_hover(self.google_map_btn, "Google-map", self.google_map_btn_img_grey))
		self.google_map_btn.place(x=20, y=self.height - 85, width=30, height=30)

		self.google_sat_btn_img_grey = ImageTk.PhotoImage(file=resource_path(f"data\\google-satellite-grey.png"))
		self.google_sat_btn_img_lightgrey = ImageTk.PhotoImage(file=resource_path(f"data\\google-satellite-lightgrey.png"))
		self.google_sat_btn = tkinter.Label(self.root, image=self.google_sat_btn_img_grey if self.map_server != "Google-satellite" else self.google_sat_btn_img_lightgrey, borderwidth=0, highlightthickness=0, cursor="hand2")
		self.google_sat_btn.bind("<Button-1>", lambda event: self.map_change(self.google_sat_btn, "Google-satellite"))
		self.google_sat_btn.bind("<Enter>", lambda event: self.map_change_hover(self.google_sat_btn, "Google-satellite", self.google_sat_btn_img_lightgrey))
		self.google_sat_btn.bind("<Leave>", lambda event: self.map_change_hover(self.google_sat_btn, "Google-satellite", self.google_sat_btn_img_grey))
		self.google_sat_btn.place(x=20, y=self.height - 50, width=30, height=30)

		self.overlay_btn_img_grey = ImageTk.PhotoImage(file=resource_path(f"data\\layers-grey.png"))
		self.overlay_btn_img_lightgrey = ImageTk.PhotoImage(file=resource_path(f"data\\layers-lightgrey.png"))
		self.overlay_btn = tkinter.Label(self.root, image=self.overlay_btn_img_lightgrey if self.overlay_active else self.overlay_btn_img_grey, borderwidth=0, highlightthickness=0, cursor="hand2")
		self.overlay_btn.bind("<Button-1>", lambda event: self.overlay_change(self.overlay_btn))
		self.overlay_btn.bind("<Enter>", lambda event: self.overlay_change_hover(self.overlay_btn, self.overlay_btn_img_lightgrey))
		self.overlay_btn.bind("<Leave>", lambda event: self.overlay_change_hover(self.overlay_btn, self.overlay_btn_img_grey))
		self.overlay_btn.place(x=20, y=self.height - 170, width=30, height=30)

	def resize(self, event):
		if event.widget == self.root and (event.width != self.width or event.height != self.height):
			self.width = event.width
			self.height = event.height

			try:
				self.google_sat_btn.place(x=20, y=self.height - 50)
				self.google_map_btn.place(x=20, y=self.height - 85)
				self.osm_btn.place(x=20, y=self.height - 120)
				self.overlay_btn.place(x=20, y=self.height - 170)
			except AttributeError:
				pass
				# this might get called while starting the app before the buttons are created, so this will catch that error

	def map_change(self, widget, server):
		if self.map_server != server:
			self.map.change_map(MAP_SERVERS[server])

			match server:
				case "OpenStreetMap":
					widget.configure(image=self.osm_btn_img_lightgrey)
				case "Google-map":
					widget.configure(image=self.google_map_btn_img_lightgrey)
				case "Google-satellite":
					widget.configure(image=self.google_sat_btn_img_lightgrey)

			match self.map_server:
				case "OpenStreetMap":
					self.osm_btn.configure(image=self.osm_btn_img_grey)
				case "Google-map":
					self.google_map_btn.configure(image=self.google_map_btn_img_grey)
				case "Google-satellite":
					self.google_sat_btn.configure(image=self.google_sat_btn_img_grey)

			self.map_server = server

	def map_change_hover(self, widget, server, img):
		if self.map_server != server:
			widget.configure(image=img)

	def overlay_change(self, widget):
		if self.overlay_active:
			widget.configure(image=self.overlay_btn_img_grey)
			self.overlay_active = False
			self.map.change_overlay("")
		else:
			widget.configure(image=self.overlay_btn_img_lightgrey)
			self.overlay_active = True
			self.map.change_overlay(OVERLAY_SERVER)

	def overlay_change_hover(self, widget, img):
		if not self.overlay_active:
			widget.configure(image=img)


MAP_SERVERS = {
	"OpenStreetMap": "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
	"Google-map": "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
	"Google-satellite": "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
}
OVERLAY_SERVER = f"file://{resource_path('data/river_overlay/{z}/{x}/{y}.png')}"
MREZNICA_DATA = load_json(resource_path("data\\mreznica.json"))


"""
marker = map_widget.set_marker(45.5981525, 15.7563562, "test", icon=icon1, icon_anchor="s")
#marker.change_icon(icon)
#marker.command = testt

marker2 = map_widget.set_marker(45.0, 45.001, "test")
# marker2.image = img
marker2.image_zoom_visibility = (10, float("inf"))
marker2.icon = icon2
"""


def main():
	root = tkinter.Tk()
	App(root)
	root.mainloop()


if __name__ == "__main__":
	main()
