import matplotlib
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from numpy import equal
#plt.style.use('seaborn-white')

class Plot2D:

    def __init__(self, room, view, slice, p):
        self.view = view
        self.slice = slice
        self.p = p

        self.res = 3 #resolution, steps per dimension value
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.sensorLocations = []
        self.sensorValues = []
        self.updateSensorLocations(room)
        self.updateDimensions(room)

    def update(self, room):
        self.updateSensorLocations(room)
        self.updateDimensions(room)
        self.updateIDW()

    def updateSensorLocations(self, room):
        self.sensorLocations = []

        for sensor in room.getSensorList():
            sX, sY, sZ = sensor.getLocation()
            if self.view == 0:
                temp = [sX, sY, sZ]
            elif self.view == 1:
                temp = [sX, sZ, sY]
            else:
                temp = [sY, sZ, sX]
            self.sensorLocations.append(temp)
        
        self.updateSensorValues(room)
            

    def updateSensorValues(self, room):
        self.sensorValues = []

        for sensor in room.getSensorList():
            self.sensorValues.append(sensor.getValue())

    def updateDimensions(self, room):
        if self.view == 0:
            self.l, self.w, h = room.getDimensions()
        elif self.view == 1:
            self.l, h, self.w = room.getDimensions()
        else:
            h, self.l, self.w = room.getDimensions()

        self.x = np.linspace(0, self.l, self.l*self.res)
        self.y = np.linspace(0, self.w, self.w*self.res)
        self.X, self.Y = np.meshgrid(self.x, self.y)

    def setSlice(self, slice):
        self.slice = slice

    def setP(self, p):
        self.p = p
        
    def updateIDW(self):
        Z = []
        for indey, yC in enumerate(self.y):
            Z.append([])
            for xC in self.x:
                arr = Z[int(indey)]                
                arr.append(self.calcPointValue(xC, yC))

        self.ax.clear()
        # self.fig.colorbar()
        self.ax.set_xlim([0, self.l])
        self.ax.set_ylim([0, self.w])
        self.ax.contourf(self.X, self.Y, Z, 50, cmap='viridis', vmin=0, vmax=1)
        self.ax.set_aspect('equal', 'box')

        if self.view == 0:
            self.ax.set_title("IDW Hydrogen concentration, p: " + str(self.p) + ", at height: " + str(self.slice))
            self.ax.set_xlabel("Length")
            self.ax.set_ylabel("Width")
        elif self.view == 1:
            self.ax.set_title("IDW Hydrogen concentration, p: " + str(self.p) + ", at width: " + str(self.slice))
            self.ax.set_xlabel("Length")
            self.ax.set_ylabel("Height")
        else:
            self.ax.set_title("IDW Hydrogen concentration, p: " + str(self.p) + ", at length: " + str(self.slice))
            self.ax.set_xlabel("Width")
            self.ax.set_ylabel("Height")
 
    def calcPointValue(self, x, y):
        
        A = 0
        B = 0
        for index, sensor in enumerate(self.sensorLocations):
            C = 1/np.power(self.distance(x, y, self.slice, sensor), self.p)
            A += C*self.sensorValues[index]
            B += C

        return A / B

    def distance(self, x, y, z, other):
        return np.sqrt(np.sum(np.square(np.array([x, y, z]) - np.array(other))))

    #def view2D(self, room, slice, p):       
        
        #ax.clim(0,1)
        #ax.colorbar(ticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

    def getFig(self):
        return self.fig


class Plot3D:
    # initialize the room 
    def __init__(self, l, w, h):
        self.sensors = {}
        self.obstacles = {}
        self.fig = Figure(facecolor='xkcd:brown', dpi=100)

        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fig.tight_layout()
        self.l = l
        self.w = w
        self.h = h

        self.ax.grid(False)
        self.ax.set_facecolor('xkcd:brown')
        self.updateRoom(l, w, h)
    
    def getFig(self):
        return self.fig

    # method to update the room
    def updateRoom(self, l, w, h):
        self.l = l
        self.w = w
        self.h = h
        
    def setRoomAxis(self, l, w, h):
        self.ax.grid(False)
        self.ax.set_facecolor('xkcd:brown')
        self.ax.set_xlim([0, l])
        self.ax.set_ylim([0, w])
        self.ax.set_zlim([0, h])
        self.ax.set_box_aspect(aspect=(l, w, h))

    # method to add a sensor to the graph
    def addSensor(self, sensorId, x, y, z):
        #print("wtf")
        self.sensors[int(sensorId)] = {}
        self.sensors[int(sensorId)]['x'] = x
        self.sensors[int(sensorId)]['y'] = y
        self.sensors[int(sensorId)]['z'] = z
        self.sensors[int(sensorId)]['value'] = 0.
    
    def plotSensors(self):
        for sensorId, sensorData in self.sensors.items():
            #print("test")
            if sensorData['value'] < 0.1:
                self.ax.plot(sensorData['x'], sensorData['y'], sensorData['z'], 'o',color='#95A5A6',markersize=5)
            if sensorData['value'] > 0.1:
                self.ax.plot(sensorData['x'], sensorData['y'], sensorData['z'], 'o',color='g',markersize=10)
            if sensorData['value'] > 0.2:
                self.ax.plot(sensorData['x'], sensorData['y'], sensorData['z'], 'o',color='b',markersize=20)
            if sensorData['value'] > 0.4:
                self.ax.plot(sensorData['x'], sensorData['y'], sensorData['z'], 'o',color='#FF5733',markersize=40)
            if sensorData['value'] > 0.6:
                self.ax.plot(sensorData['x'], sensorData['y'], sensorData['z'], 'o',color='r',markersize=60)
                

    # method to update a sensor in the graph
    def updateSensor(self, sensorId, x, y, z):
        self.sensors[int(sensorId)]['x'] = x
        self.sensors[int(sensorId)]['y'] = y
        self.sensors[int(sensorId)]['z'] = z

    # method to add an obstacle to the graph
    def addObstacle(self, obstacleId, x1, y1, z1, x2, y2, z2):
        self.obstacles[obstacleId] = {}
        self.obstacles[obstacleId]['positions'] = (x1,y1,z1)
        self.obstacles[obstacleId]['sizes'] = (x2,y2,z2)

    # method to update an obstacle in the graph
    def updateObstacle(self, obstacleId, x1, y1, z1, x2, y2, z2):
        self.obstacles[obstacleId]['positions'] = (x1,y1,z1)
        self.obstacles[obstacleId]['sizes'] = (x2,y2,z2)
    
    def plotObstacles(self):
        for obstacleId, obstacle in self.obstacles.items():
            self.plotCubeAt(pos=obstacle['positions'], size=obstacle['sizes'], ax=self.ax)

    # method to update sensor values in the graph
    def updateSensorData(self, sensorId, sensorValue):
        self.sensors[int(sensorId)]['value'] = sensorValue


    def cuboid_data(self, o, size=(1,1,1)):
        #print(size)
        l, w, h = size
        x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],  
            [o[0], o[0] + l, o[0] + l, o[0], o[0]],  
            [o[0], o[0] + l, o[0] + l, o[0], o[0]],  
            [o[0], o[0] + l, o[0] + l, o[0], o[0]]]  
        y = [[o[1], o[1], o[1] + w, o[1] + w, o[1]],  
            [o[1], o[1], o[1] + w, o[1] + w, o[1]],  
            [o[1], o[1], o[1], o[1], o[1]],          
            [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]]   
        z = [[o[2], o[2], o[2], o[2], o[2]],                       
            [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],   
            [o[2], o[2], o[2] + h, o[2] + h, o[2]],               
            [o[2], o[2], o[2] + h, o[2] + h, o[2]]]               
        return np.array(x), np.array(y), np.array(z)

    def plotCubeAt(self, pos=(0,0,0), size=(1,1,1), ax=None,**kwargs):
        # Plotting a cube element at position pos
        if ax !=None:
            X, Y, Z = self.cuboid_data(pos, size )
            plot = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, **kwargs)
            return plot

    def animate(self, i):
        self.ax.clear()
        #print(self.sensors)
        self.setRoomAxis(self.l, self.w, self.h)
        self.plotSensors()
        self.plotObstacles()