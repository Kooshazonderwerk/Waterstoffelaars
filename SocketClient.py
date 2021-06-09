from threading import Thread
import time
import random


class SocketClient(Thread):

    def __init__(self, serverUrl, program, room):
        self.program = program
        self.serverUrl = serverUrl
        self.room = room
        self.running = False
        self.counter = 0
        Thread.__init__(self)
        self.getRoomData()

    def run(self):
        self.running = True
        while self.running:
            time.sleep(1)
            self.counter += 1
            self.updateSensorValue()
            self.updateRoomData()
            print('test123')

    def updateSensorValue(self):
        sensorValues = []
        for sensor in self.room.getSensors():
            sensorValues.append({'id':sensor.getId(),
            'value':random.random()})
        self.program.updateSensorValue(self.room.getId(), sensorValues)
    
    def stopThread(self):
        self.running = False

    def updateRoomData(self):
        roominfo = self.getRoomData()
        self.program.updateRoomData(self.room.getId(), roominfo)

    def getRoomData(self):
        # print(dir(self.room))
        return {
            'height': 100, 
            'id': self.counter, 
            'length': 100, 
            'name': 'test', 
            'obstacles': [], 
            'sensors': [{
                'id': 1, 
                'name': str(self.counter), 
                'x': 30, 
                'y': 20, 
                'z': 10}, 
                {
                'id': 2, 
                'name': 'test', 
                'x': 32, 
                'y': 23, 
                'z': 23}, 
                {
                'id': 3, 
                'name': 'test', 
                'x': 36, 
                'y': 23, 
                'z': 23}, 
                {
                'id': 4, 
                'name': 'test', 
                'x': 12, 
                'y': 12, 
                'z': 12}, 
                {
                'id': 5, 
                'name': 
                'test', 
                'x': 21, 
                'y': 24, 
                'z': 23}], 
            'width': 100}
    
    