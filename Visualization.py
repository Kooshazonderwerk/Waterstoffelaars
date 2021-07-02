import matplotlib
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from numpy import equal
#plt.style.use('seaborn-white')

class Plot2D:

    def __init__(self, xAxis, yAxis, view, slice, p):
        self.view = view
        self.slice = slice
        self.p = p
        
        self.xAxis = xAxis
        self.yAxis = yAxis

        self.sensors = {}
        self.obstacles = {}

        self.res = 50/xAxis #resolution, steps per dimension value
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        data = [[0, 1],[0, 1]]
        cax = self.ax.imshow(data, cmap='viridis')
        cbar = self.fig.colorbar(cax, ticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        cbar.ax.set_yticklabels(['0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1'])

        self.updateDimensions()
        
        if self.view == 0:
            self.fig.suptitle("IDW Hydrogen concentration, p: " + str(self.p) + ", at height: " + str(self.slice))
            self.fig.supxlabel("Length")
            self.fig.supylabel("Width")
        elif self.view == 1:
            self.fig.suptitle("IDW Hydrogen concentration, p: " + str(self.p) + ", at width: " + str(self.slice))
            self.fig.supxlabel("Length")
            self.fig.supylabel("Height")
        else:
            self.fig.suptitle("IDW Hydrogen concentration, p: " + str(self.p) + ", at length: " + str(self.slice))
            self.fig.supxlabel("Width")
            self.fig.supylabel("Height")
        

    def updateRoom(self, xAxis, yAxis):
        self.xAxis = xAxis
        self.yAxis = yAxis
    
    def addSensor(self, sensorId, x, y, z):
        self.sensors[int(sensorId)] = {}
        self.sensors[int(sensorId)]['x'] = x
        self.sensors[int(sensorId)]['y'] = y
        self.sensors[int(sensorId)]['z'] = z
        self.sensors[int(sensorId)]['value'] = 0.
    
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
    
    def updateSensorData(self, sensorId, sensorValue):
        self.sensors[int(sensorId)]['value'] = sensorValue
    

    def updateDimensions(self):
        self.x = np.linspace(0, self.xAxis, int(self.xAxis*self.res))
        self.y = np.linspace(0, self.yAxis, int(self.yAxis*self.res))
        self.X, self.Y = np.meshgrid(self.x, self.y)

    # method draw room:
    def setRoomAxis(self):
        self.ax.set_xlim([0, self.xAxis])
        self.ax.set_ylim([0, self.yAxis])
        self.ax.set_aspect('equal', 'box')
    
    # method to draw data:
    def plotData(self):
        Z = []
        if self.sensors != {}:
            for indey, yC in enumerate(self.y):
                Z.append([])
                for xC in self.x:
                    arr = Z[int(indey)]         
                    arr.append(self.calcPointValue(xC, yC))
        else:
            Z = self.X
        self.ax.contourf(self.X, self.Y, Z, 50, cmap='viridis', vmin=0, vmax=1)


    def animate(self, i):
        self.ax.clear()
        self.setRoomAxis()
        self.plotData()

    def setSlice(self, slice):
        self.slice = slice
        self.updateTitle()

    def setP(self, p):
        self.p = p
        self.updateTitle()
    
    def updateTitle(self):
        if self.view == 0:
            self.fig.suptitle("IDW Hydrogen concentration, p: " + str(self.p) + ", at height: " + str(self.slice))
        elif self.view == 1:
            self.fig.suptitle("IDW Hydrogen concentration, p: " + str(self.p) + ", at width: " + str(self.slice))
        else:
            self.fig.suptitle("IDW Hydrogen concentration, p: " + str(self.p) + ", at length: " + str(self.slice))
 
    def calcPointValue(self, x, y):
        
        A = 0
        B = 0
        for index, sensor in self.sensors.items():
            C = 1/np.power(self.distance(x, y, self.slice, [sensor['x'],sensor['y'],sensor['z']]), self.p)
            A += C*sensor['value']
            B += C

        return A / B

    def distance(self, x, y, z, other):
        return np.sqrt(np.sum(np.square(np.array([x, y, z]) - np.array(other))))

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
    
    '''returns a Figure that is holded by the Plot3D object'''
    def getFig(self):
        return self.fig

    '''takes int, int, int and updates the dimensions on the Plot3D object to set te room size'''
    def updateRoom(self, l, w, h):
        self.l = l
        self.w = w
        self.h = h


    '''takes int, int, int and updates the plot room size'''
    def setRoomAxis(self, l, w, h):
        self.ax.grid(False)
        self.ax.set_facecolor('xkcd:brown')
        self.ax.set_xlim([0, l])
        self.ax.set_ylim([0, w])
        self.ax.set_zlim([0, h])
        self.ax.set_box_aspect(aspect=(l, w, h))

    '''takes int, int, int, int and adds it to a list of sensors'''
    def addSensor(self, sensorId, x, y, z):
        self.sensors[int(sensorId)] = {}
        self.sensors[int(sensorId)]['x'] = x
        self.sensors[int(sensorId)]['y'] = y
        self.sensors[int(sensorId)]['z'] = z
        self.sensors[int(sensorId)]['value'] = 0.
    
    '''plots all sensors on the Plot3D object'''
    def plotSensors(self):
        for sensorId, sensorData in self.sensors.items():
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
                

    '''takes int, int, int, int and updates the sensor with the given sensor id in the list with sensors'''
    def updateSensor(self, sensorId, x, y, z):
        self.sensors[int(sensorId)]['x'] = x
        self.sensors[int(sensorId)]['y'] = y
        self.sensors[int(sensorId)]['z'] = z

    '''takes int, int, int, int and adds it to a list of obstacles'''
    def addObstacle(self, obstacleId, x1, y1, z1, x2, y2, z2):
        self.obstacles[obstacleId] = {}
        self.obstacles[obstacleId]['positions'] = (x1,y1,z1)
        self.obstacles[obstacleId]['sizes'] = (x2,y2,z2)

    '''takes int, int, int, int and updates the obstacle with the given obstacle id in the list with obstacles'''
    def updateObstacle(self, obstacleId, x1, y1, z1, x2, y2, z2):
        self.obstacles[obstacleId]['positions'] = (x1,y1,z1)
        self.obstacles[obstacleId]['sizes'] = (x2,y2,z2)
    
    '''plots all obstacles on the Plot3D object'''
    def plotObstacles(self):
        for obstacleId, obstacle in self.obstacles.items():
            self.plotCubeAt(pos=obstacle['positions'], size=obstacle['sizes'], ax=self.ax)

    '''takes int, float and updates the value of a sensor with the given sensor id'''
    def updateSensorData(self, sensorId, sensorValue):
        self.sensors[int(sensorId)]['value'] = sensorValue

    '''takes a tuple(int,int,int), tuple(int,int,int) and generates data for plotting a obstacle'''
    def cuboid_data(self, o, size=(1,1,1)):
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

    '''takes a tuple(int,int,int), tuple(int,int,int), Axis object with the current plot info and plots a obstacle'''
    def plotCubeAt(self, pos=(0, 0, 0), size=(1, 1, 1), ax=None, **kwargs):
        # Plotting a cube element at position pos
        if ax !=None:
            X, Y, Z = self.cuboid_data(pos, size )
            plot = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, **kwargs)
            return plot

    '''method is used to animate continues data'''
    def animate(self, i):
        self.ax.clear()
        self.setRoomAxis(self.l, self.w, self.h)
        self.plotSensors()
        self.plotObstacles()
