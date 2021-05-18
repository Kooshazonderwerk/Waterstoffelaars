from Sensor import Sensor

class Room:

	def __init__(self, id, lenght=0, width=0, height=0, sensors=[]):
		self.sensorList = []
		self.id = id
		self.lenght = lenght
		self.width = width
		self.height = height
		for sensor in sensors:
			self.addSensor(Sensor(sensor['id'], sensor['name'], sensor['x'], sensor['y'], sensor['z']))

	'''Takes a object of type Sensor and adds it to the list of sensors'''
	def addSensor(self, sensor):
		if(isinstance(sensor, Sensor)):
			self.sensorList.append(sensor)
		else:
			print(type(sensor)+' object is not of Type Sensor') #ERRORHANDELING

	'''returns a list with all sensors currently holded by the Room object'''
	def getSensors(self):
		return self.sensorList
	
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