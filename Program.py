from Room import Room
from Sensor import Sensor
from Obstacle import Obstacle
from SocketClientHandler import *
import threading

class Program:
	def __init__(self, gui, url):
		self.gui = gui
		self.rooms = {}
		self.sem = threading.Semaphore()
		self.socketconn = SocketClientHandler(self, url)
		print('my sid is', self.socketconn.sio.sid)


	'''Method calls the quit method of the SocketClientHandler'''
	def quit(self):
		self.socketconn.quit()
	
	'''Method returns a dict containing the list of Room objects holded by the Program'''
	def getRooms(self):
		return self.rooms

	'''Method Takes a dict containing the the room information and adds it to the Program'''
	def addRoom(self, room):
		self.rooms[room['id']] = Room(room['id'], room['name'], room['length'], room['width'], room['height']) 
	
	'''Method takes a dict of room info and updates it in the Program'''
	def updateRoom(self, room):
		self.rooms[room['id']].update(room)
	
	'''Method takes a dict of room info and checks if it exist in the Program and either adds it of updates it'''
	def handleRoom(self, room):
		self.sem.acquire()
		if room['id'] in self.rooms:
			self.updateRoom(room)
		else:
			self.addRoom(room)
		self.gui.updateRoomData(self.getRoom(room['id']))
		self.sem.release()
	
	'''Method takes String, int,int,int and sends the info to the SocketClientHandler to create a room on the server'''
	def createRoom(self, name, width, height, length):
		self.socketconn.createRoom(name, width, height, length)
	
	'''Method takes int, String, int, int,int and sends the info to the SocketClientHandler to update a room on the server'''
	def editRoom(self, id, name, width, height, length):
		self.socketconn.editRoom(id, name, width, height, length)

	#Sensors
	'''Method takes a dict containing sensor info and checks if it exist in the Program and either adds it of updates it'''
	def handleSensor(self, sensor):
		self.sem.acquire()
		result = self.rooms[sensor['roomId']].getSensor(sensor['id'])
		if result == None:
			self.addSensor(sensor, sensor['roomId'])
		else:
			self.updateSensor(sensor, sensor['roomId'])
		room = self.getRoom(sensor['roomId'])
		self.gui.updateSensorData(room.getSensor(sensor['id']), room)
		self.sem.release()
	
	'''Method takes a dict, int dict contains sensor info and adds it in the Program'''
	def addSensor(self, sensor, roomId):
		self.rooms[roomId].addSensor(Sensor(sensor['id'], sensor['name'], sensor['x'], sensor['y'], sensor['z']))

	'''Method takes a dict, int dict contains sensor info and updates it in the Program'''
	def updateSensor(self, sensor, roomId):
		self.rooms[roomId].updateSensor(sensor)
        
	#Obstacles
	
	'''Method takes a dict containing obstacle info and checks if it exist in the Program and either adds it of updates it'''
	def handleObstacle(self, obstacle):
		self.sem.acquire()
		result = self.rooms[obstacle['roomId']].getObstacle(obstacle['id'])
		if result == None:
			self.addObstacle(obstacle, obstacle['roomId'])
		else:
			self.updateObstacle(obstacle, obstacle['roomId'])
		room = self.getRoom(obstacle['roomId'])
		self.gui.updateObstacleData(room.getObstacle(obstacle['id']), room)
		self.sem.release()
	
	'''Method takes a dict, int. the dict contains obstacle info and adds it in the Program'''
	def addObstacle(self, obstacle, roomId):
		self.rooms[roomId].addObstacle(Obstacle(obstacle['id'], obstacle['name'], obstacle['x1'], obstacle['y1'], obstacle['z1'], obstacle['x2'], obstacle['y2'], obstacle['z2']))

	'''Method takes a dict, int. the dict contains obstacle info and updates it in the Program'''
	def updateObstacle(self, obstacle, roomId):
		self.rooms[roomId].updateObstacle(obstacle)

	'''Method takes int, String, int, int, int and sends the info to the SocketClientHandler to create a sensor on the server'''
	def createSensor(self, roomId, name, x, y, z):
		self.socketconn.createSensor(roomId, name, x, y, z)

	'''Method takes int, String, int, int, int and sends the info to the SocketClientHandler to update a sensor on the server'''
	def editSensor(self, id, name, x, y, z):
		self.socketconn.editSensor(id, name, x, y, z)

	'''Method takes int, String, int, int, int, int, int, int and sends the info to the SocketClientHandler to create a obstacle on the server'''
	def createObstacle(self, roomId, name, x1, y1, z1, x2, y2, z2):
		self.socketconn.createObstacle(roomId, name, x1, y1, z1, x2, y2, z2)

	'''Method takes int, String, int, int, int, int, int, int and sends the info to the SocketClientHandler to update a obstacle on the server'''
	def editObstacle(self, id, name, x1, y1, z1, x2, y2, z2):
		self.socketconn.editObstacle(id, name, x1, y1, z1, x2, y2, z2)

	'''method takes a dict containing sensor values and sends it to the gui to be displayed'''
	def updateSensorValues(self, sensorValues):
		for sensorId, sensorValue in sensorValues.items():
			room = self.getRoom(sensorValue['room_id'])
			if room is not None: # sensor values can be send before a room and sensor is added to the program to prevent errors this method checks whether or not they exist
				sensor = room.getSensor(int(sensorId))
				if sensor is not None:
					sensor.setValue(sensorValue['value'])
					self.gui.updateSensorValues(sensorValues)
	
	'''method takes an int and returns a corresponding room'''
	def getRoom(self, roomId):
		if roomId in self.rooms:
			return self.rooms[roomId]
		return None