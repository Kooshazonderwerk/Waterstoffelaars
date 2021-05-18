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

	def addSensor(self, roomId, name, x, y, z):
		rawData = {
			'name': name,
			'x': x,
			'y': y,
			'z': z
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