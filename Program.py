from Room import Room
from Sensor import Sensor
from Obstacle import Obstacle
from Network import Network
from SocketClient import SocketClient
from SocketClientHandler import *
import threading

class Program:
	def __init__(self, gui, url):
		self.gui = gui
		self.rooms = {}
		self.network = Network(url)
		self.roomCount = 0
		self.sem = threading.Semaphore()
		# self.webSockets = []
		# self.addRoomsFromNetwork()
		self.socketconn = SocketClientHandler(self)
		print('my sid is', self.socketconn.sio.sid)
		# for key in self.rooms:
		# 	self.webSockets.append(SocketClient(url, self, self.rooms[key], self.socketconn))


	# Rooms
	def getRooms(self):
		return self.rooms

	def addRoom(self, room):
		self.rooms[room['id']] = Room(room['id'], room['name'], room['length'], room['width'], room['height']) 

	def addRooms(self, rooms):
		for room in rooms:
			self.addRoom(room)
		
	def updateRoom(self, room):
		self.rooms[room['id']].update(room)
	
	def handleRoom(self, room):
		self.sem.acquire()
		if room['id'] in self.rooms:
			self.updateRoom(room)
		else:
			self.addRoom(room)
		self.gui.updateRoomData(self.getRoom(room['id']))
		self.sem.release()
	
	def updateRooms(self, rooms):
		self.addRooms(rooms)
		self.gui.updateRooms()

	def createRoom(self, name, width, height, length):
		self.network.createRoom(name, width, height, length)
	
	def editRoom(self, id, name, width, height, length):
		self.network.editRoom(id, name, width, height, length)

	#Sensors

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
	
	def addSensor(self, sensor, roomId):
		self.rooms[roomId].addSensor(Sensor(sensor['id'], sensor['name'], sensor['x'], sensor['y'], sensor['z']))

	def updateSensor(self, sensor, roomId):
		self.rooms[roomId].updateSensor(sensor)
        
	#Obstacles
	
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
	
	def addObstacle(self, obstacle, roomId):
		self.rooms[roomId].addObstacle(Obstacle(obstacle['id'], obstacle['name'], obstacle['x1'], obstacle['y1'], obstacle['z1'], obstacle['x2'], obstacle['y2'], obstacle['z2']))

	def updateObstacle(self, obstacle, roomId):
		self.rooms[roomId].updateObstacle(obstacle)


	def editSensor(self, id, name, x, y, z):
		self.network.editSensor(id, name, x, y, z)

	def editObstacle(self, id, name, x1, y1, z1, x2, y2, z2):
		self.network.editObstacle(id, name, x1, y1, z1, x2, y2, z2)


	def updateSensorValues(self, sensorValues):
		self.gui.updateSensorValues(sensorValues)
	
	# def startThreads(self):
	# 	for t in self.webSockets:
	# 		t.start()
	
	def updateRoomData(self, roomId, roomInfo):
		newRoom = Room(roomInfo[' id'], roomInfo['name'], roomInfo['length'], roomInfo['width'], roomInfo['height'], roomInfo['sensors'], roomInfo['obstacles'])
		self.rooms[roomId] = newRoom
		self.gui.updateRoomData(roomId, roomInfo)
	
	def getRoom(self, roomId):
		return self.rooms[roomId]