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