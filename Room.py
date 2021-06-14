from Sensor import Sensor
from Obstacle import Obstacle

class Room:

	def __init__(self, id, name, lenght=0, width=0, height=0, sensors=[], obstacles=[]):
		self.obstacleList = []
		self.sensorList = []
		self.id = id
		self.name = name
		self.lenght = lenght
		self.width = width
		self.height = height
		for sensor in sensors:
			self.addSensor(Sensor(sensor['id'], sensor['name'], sensor['x'], sensor['y'], sensor['z']))
		for obstacle in obstacles:
			self.addObstacle(Obstacle(obstacle['id'], obstacle['name'], obstacle['x1'], obstacle['y1'], obstacle['z1'], obstacle['x2'], obstacle['y2'], obstacle['z2']))

	'''Takes a object of type Sensor and adds it to the list of sensors'''
	def addSensor(self, sensor):
		if(isinstance(sensor, Sensor)):
			self.sensorList.append(sensor)
		else:
			print(type(sensor)+' object is not of Type Sensor') #ERRORHANDELING

	'''returns a list with all sensors currently holded by the Room object'''
	def getSensors(self):
		return self.sensorList
		
	'''takes a sensor id and returns the corresponding sensor'''
	def getSensor(self, sensorId):
		for sensor in self.sensorList:
			if(sensor.getId() == sensorId):
				return sensor
		print('error: no sensor found with id: '+ sensorId) #ERRORHANDELING
		return None

	'''Takes a object of type Obstacle and adds it to the list of obstacles'''
	def addObstacle(self, obstacle):
		if(isinstance(obstacle, Obstacle)):
			self.obstacleList.append(obstacle)
		else:
			print(type(obstacle)+' object is not of Type Obstacle') #ERRORHANDELING

	'''returns a list with all obstacles currently holded by the Room object'''
	def getObstacles(self):
		return self.obstacleList
	
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