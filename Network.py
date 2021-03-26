import requests
import json

class Network:

	def __init__(self, url):
		self.url = url

	def getRooms(self):
		rooms = requests.get(self.url+'/room/all').json()
		return rooms
