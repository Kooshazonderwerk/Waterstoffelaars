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
		self.socketconn = SocketClientHandler(self)
		print('my sid is', self.socketconn.sio.sid)


	def quit(self):
		self.socketconn.quit()
	# Rooms
	def getRooms(self):
		return self.rooms

	def addRoom(self, room):
		self.rooms[room['id']] = Room(room['id'], room['name'], room['length'], room['width'], room['height']) 
		
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
	

	def createRoom(self, name, width, height, length):
		self.socketconn.createRoom(name, width, height, length)
	
	def editRoom(self, id, name, width, height, length):
		self.socketconn.editRoom(id, name, width, height, length)

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

	def createSensor(self, roomId, name, x, y, z):
		self.socketconn.createSensor(roomId, name, x, y, z)

	def editSensor(self, id, name, x, y, z):
		self.socketconn.editSensor(id, name, x, y, z)

	def createObstacle(self, roomId, name, x1, y1, z1, x2, y2, z2):
		self.socketconn.createObstacle(roomId, name, x1, y1, z1, x2, y2, z2)

	def editObstacle(self, id, name, x1, y1, z1, x2, y2, z2):
		self.socketconn.editObstacle(id, name, x1, y1, z1, x2, y2, z2)


	def updateSensorValues(self, sensorValues):
		for sensorId, sensorValue in sensorValues.items():
			room = self.getRoom(sensorValue['room_id'])
			if room is not None:
				sensor = room.getSensor(int(sensorId))
				if sensor is not None:
					sensor.setValue(sensorValue['value'])
					self.gui.updateSensorValues(sensorValues)
	
	
	def getRoom(self, roomId):
		if roomId in self.rooms:
			return self.rooms[roomId]
		return None