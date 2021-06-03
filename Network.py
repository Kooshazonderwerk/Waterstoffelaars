import requests
import json

class Network:

	def __init__(self, url):
		self.url = url

	def getRooms(self):
		rooms = requests.get(self.url+'/room/all').json()
		print(rooms)
		return rooms
	
	def createRoom(self, name, width, height, length):
		rawData = {
			'name': name,
			'width': width,
			'length': length,
			'height': height,
		}
		data = json.dumps(rawData)
		requests.post(self.url+'/room', json=rawData)

	def editRoom(self, id, name, width, height, length):
		rawData = {
			'name': name,
			'width': width,
			'length': length,
			'height': height,
		}
		data = json.dumps(rawData)
		requests.put(self.url+'/room/'+str(id), json=rawData)



	def addSensor(self, roomId, name, x, y, z):
		rawData = {
			'type': "sensor",
			'name': name,
			'x': x,
			'y': y,
			'z': z
		}
		data = json.dumps(rawData)
		print(data)
		requests.post(self.url+'/room/'+str(roomId), json=rawData)
	
	def addObstacle(self, roomId, name, x1, y1, z1, x2, y2, z2):
		rawData = {
			'type': "obstacle",
			'name': name,
			'x1': x1,
			'y1': y1,
			'z1': z1,
			'x2': x2,
			'y2': y2,
			'z2': z2
		}
		data = json.dumps(rawData)
		print(data)
		requests.post(self.url+'/room/'+str(roomId), json=rawData)

	def editSensor(self, id, name, x, y, z):
		rawData = {
			'name': name,
			'x': x,
			'y': y,
			'z': z
		}
		data = json.dumps(rawData)
		print(data)
		requests.put(self.url+'/sensor/'+str(id), json=rawData)

	def editObstacle(self, id, name, x1, y1, z1, x2, y2, z2):
		rawData = {
			'name': name,
			'x1': x1,
			'y1': y1,
			'z1': z1,
			'x2': x2,
			'y2': y2,
			'z2': z2
		}
		data = json.dumps(rawData)
		print(data)
		requests.put(self.url+'/obstacle/'+str(id), json=rawData)