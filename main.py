import tkinter as tk
from Room import Room
from Sensor import Sensor
from Program import Program
from GuiPages import *

CLIENT_NAME = "waterstoffelaars"
PAGES = (
	StartPage,
	EditRoomPage,
	EditSensorPage
)
SERVER_URL = "http://localhost:5000"

class Gui(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.value = ""

		tk.Tk.wm_title(self, CLIENT_NAME)
		container = tk.Frame(self)

		container.pack(side="top", fill="both", expand = True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		self.program = Program(SERVER_URL)
		self.frames = {}

		for page in PAGES:
			frame = page(container, self)

			self.frames[page] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	def show_frame(self, cont, post=None):
		frame = self.frames[cont]
		frame.tkraise()
		if cont == StartPage:
			frame.reload()
		if post is not None:
			frame.post(post)
		return frame
	
	def setValue(self, value):
		self.value = value
	
	def getValue(self):
		return self.value


	


gui = Gui()
gui.mainloop()