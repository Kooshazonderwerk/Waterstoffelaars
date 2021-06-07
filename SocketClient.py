from threading import Thread
import time
import random


class SocketClient(Thread):

    def __init__(self, serverUrl, program, roomId):
        self.program = program
        self.serverUrl = serverUrl
        self.roomId = roomId
        self.running = False
        Thread.__init__(self)

    def run(self):
        self.running = True
        while self.running:
            time.sleep(1)
            self.updateSensorData()
            print('test123')

    def updateSensorData(self):
        sensorValues = []
        sensorValues.append(random.random())
        self.program.updateSensorData(self.roomId, sensorValues)
    
    def stopThread(self):
        self.running = False