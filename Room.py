from Sensor import Sensor
from Obstacle import Obstacle

class Room:

	def __init__(self, id, name, lenght=0, width=0, height=0, sensors=[], obstacles=[]):
		self.obstacleList = {}
		self.sensorList = {}
		self.id = id
		self.name = name
		self.lenght = lenght
		self.width = width
		self.height = height

	'''Takes a object of type Sensor and adds it to the dict of sensors'''
	def addSensor(self, sensor):
		if(isinstance(sensor, Sensor)):
			self.sensorList[sensor.id] = sensor
		else:
			print(str(type(sensor))+' object is not of Type Sensor') #ERRORHANDELING

	'''returns a dict with all sensors currently holded by the Room object'''
	def getSensors(self):
		return self.sensorList
	
	'''returns list with all obstacles currently holded by the Room object'''
	def getSensorList(self):
		response = []
		for key, value in self.sensorList.items():
			response.append(value)
		return response
			
	'''Takes a object of type Sensor and updates it in the dict of sensors'''
	def updateSensor(self, sensor):
		self.sensorList[sensor['id']].update(sensor)

	'''takes a sensor id and if it exist returns the corresponding sensor else it returns none'''
	def getSensor(self, sensorId):
		if sensorId in self.sensorList:
			return self.sensorList[sensorId]
		return None

	'''Takes a object of type Obstacle and adds it to the dict of obstacles'''
	def addObstacle(self, obstacle):
		if(isinstance(obstacle, Obstacle)):
			self.obstacleList[obstacle.id] = obstacle
		else:
			print(str(type(obstacle))+' object is not of Type Obstacle') #ERRORHANDELING

	'''Takes a object of type Obstacle and updates it in the dict of obstacles'''
	def updateObstacle(self, obstacle):
		self.obstacleList[obstacle['id']].update(obstacle)
	
	'''takes a sensor id and if it exist returns the corresponding sensor else it returns none'''
	def getObstacle(self, obstacleId):
		if obstacleId in self.obstacleList:
			return self.obstacleList[obstacleId]
		return None

	'''returns a dict with all obstacles currently holded by the Room object'''
	def getObstacles(self):
		return self.obstacleList

	'''returns list with all obstacles currently holded by the Room object'''
	def getObstacleList(self):
		response = []
		for key, value in self.obstacleList.items():
			response.append(value)
		return response
	
	'''returns a tuple with 3 ints containing the current stored size of the Room object'''
	def getDimensions(self):
		return (self.lenght, self.width, self.height)

	'''Takes 3 ints and changes the current stored size of the Room object'''
	def setDimensions(self, lenght, width, height):
		self.lenght = lenght
		self.width = width
		self.height = height

	'''returns a string with the id stored in the Room object'''
	def getId(self):
		return self.id
	
	'''returns a string with the stored name'''
	def getName(self):
		return self.name
	
	'''takes a dict containing room info and updates itself'''
	def update(self, room):
		self.name = room['name']
		self.lenght = room['length']
		self.width = room['width']
		self.height = room['height']