import tkinter as tk
from Room import Room
from Sensor import Sensor
from Obstacle import Obstacle
from Program import Program
from GuiPages import *

CLIENT_NAME = "waterstoffelaars"
PAGES = (
	StartPage,
	EditRoomPage,
	EditSensorPage,
	EditObstaclePage
)
SERVER_URL = "http://localhost:5001"

class Gui(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.value = ""

		tk.Tk.wm_title(self, CLIENT_NAME)
		container = tk.Frame(self)
		self.protocol("WM_DELETE_WINDOW", self.quitMe)
		container.pack(side="top", fill="both", expand = True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		self.program = Program(self, SERVER_URL)
		self.frames = {}
		
		# Loop through a list of pages and using the class signature to create and save the corresponding page
		for page in PAGES:
			frame = page(container, self)

			self.frames[page] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	'''method is called when the program is quit'''
	def quitMe(self):
		self.program.quit()
		self.quit()
		self.destroy()
		
	'''method takes a Frame class signature and dict and returns the selected frame '''
	'''post is send to the post method of the called frame and used as post data there'''
	def show_frame(self, cont, post=None):
		frame = self.frames[cont]
		frame.tkraise()
		if post is not None:
			frame.post(post)
		return frame
	
	'''method taked a int and sets it to the gui object to be shared between frames'''
	def setValue(self, value):
		self.value = value
	
	'''returns an int that is set using setValue'''
	def getValue(self):
		return self.value

	'''takes a dict containing sensor values and passes it to the startpage frame'''
	def updateSensorValues(self, sensorValues):
		startPage = self.frames[StartPage]
		startPage.updateSensorValues(sensorValues)
	
	'''takes a Sensor and Room object and passes it to the startpage frame'''
	def updateSensorData(self, sensor, room):
		startPage = self.frames[StartPage]
		print(sensor.name)
		startPage.loadSensor(sensor, room)
	
	'''takes a Room object and passes it to the startpage frame'''
	def updateRoomData(self, room):
		startPage = self.frames[StartPage]
		startPage.loadRoom(room, room.id)

	'''takes a Obstacle and Room object and passes it to the startpage frame'''
	def updateObstacleData(self, obstacle, room):
		startPage = self.frames[StartPage]
		startPage.loadObstacle(obstacle, room)
