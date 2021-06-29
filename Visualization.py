import matplotlib
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
from numpy import equal
plt.style.use('seaborn-white')

class Visualization:

    def calcPointValue(self, sensorLocations, sensorValues, x, y, z, p):
        
        A = 0
        B = 0
        for index, sensor in enumerate(sensorLocations):
            C = 1/np.power(self.distance(x, y, z, sensor), p)
            A += C*sensorValues[index]
            B += C

        #B = 0
        #for sensor in sensorLocations:
        #    B += 1/np.power(self.distance(x, y, z, sensor), p)
    
        return A / B

    def distance(self, x, y, z, other):
        return np.sqrt(np.sum(np.square(np.array([x, y, z]) - np.array(other))))

    def view2D(self, room, slice, p, view):
        plt.close()
        fig = plt.figure()
        plt.ioff()

        res = 3 #resolution, steps per dimension value

        if view == 0:
            l, w, h = room.getDimensions()
        elif view == 1:
            l, h, w = room.getDimensions()
        else:
            h, l, w = room.getDimensions()

        x = np.linspace(0, l, l*res)
        y = np.linspace(0, w, w*res)
        X, Y = np.meshgrid(x, y)
        
        sensorLocations = []
        sensorValues = []
        for sensor in room.getSensorList():
            sX, sY, sZ = sensor.getLocation()
            if view == 0:
                temp = [sX, sY, sZ]
            elif view == 1:
                temp = [sX, sZ, sY]
            else:
                temp = [sY, sZ, sX]
            #print(temp)
            sensorLocations.append(temp)
            sensorValues.append(sensor.getValue())

        Z = []
        for indey, yC in enumerate(y):
            Z.append([])
            for xC in x:
                arr = Z[int(indey)]                
                arr.append(self.calcPointValue(sensorLocations, sensorValues, xC, yC, slice, p))
        
        plt.axes().set_aspect('equal', 'box')
        plt.contourf(X, Y, Z, 50, cmap='viridis')
        plt.clim(0,1)
        plt.colorbar(ticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        if view == 0:
            plt.title("IDW Hydrogen concentration, p: " + str(p) + ", at height: " + str(slice))
            plt.xlabel("Length")
            plt.ylabel("Width")
        elif view == 1:
            plt.title("IDW Hydrogen concentration, p: " + str(p) + ", at width: " + str(slice))
            plt.xlabel("Length")
            plt.ylabel("Height")
        else:
            plt.title("IDW Hydrogen concentration, p: " + str(p) + ", at length: " + str(slice))
            plt.xlabel("Width")
            plt.ylabel("Height") 

        return fig


class Plot3D:
    # initialize the room 
    def __init__(self, l, w, h):
        self.sensors = {}
        self.obstacles = {}
        self.fig = Figure(facecolor='xkcd:brown', dpi=100)

        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fig.tight_layout()


        self.ax.grid(False)
        self.ax.set_facecolor('xkcd:brown')
        self.updateRoom(l, w, h)
    
    def getFig(self):
        return self.fig

    # method to update the room
    def updateRoom(self, l, w, h):
        self.ax.set_xlim([0, l])
        self.ax.set_ylim([0, w])
        self.ax.set_zlim([0, h])
        self.ax.set_box_aspect(aspect=(l, w, h))

    # method to add a sensor to the graph
    def addSensor(self, sensorId, x, y, z):
        sensorPlot = self.ax.plot(x, y, z, 'o',color='#95A5A6',markersize=5) # returns a list with one plot -_-
        self.sensors[sensorId] = sensorPlot[0]

    # method to update a sensor in the graph
    def updateSensor(self, sensorId, x, y, z):
        self.sensors[sensorId].set_data_3d(x, y, z)

    # method to add an obstacle to the graph
    def addObstacle(self, obstacleId, x1, y1, z1, x2, y2, z2):
        positions = (x1,y1,z1)
        sizes = (x2,y2,z2)
        self.obstacles[obstacleId] = self.plotCubeAt(pos=positions, size=sizes, ax=self.ax)

    # method to update an obstacle in the graph
    def updateObstacle(self, obstacleId, x1, y1, z1, x2, y2, z2):
        positions = (x1,y1,z1)
        sizes = (x2,y2,z2)
        self.obstacles[obstacleId].remove()
        self.obstacles[obstacleId] = self.plotCubeAt(pos=positions, size=sizes, ax=self.ax)

    # method to update sensor values in the graph
    def updateSensorData(self, sensorId, sensorValue):
        if sensorId in self.sensors:
            if sensorValue < 0.1:
                self.sensors[sensorId].set_markersize(5)
                self.sensors[sensorId].set_markerfacecolor('#95A5A6')
            if sensorValue > 0.1:
                self.sensors[sensorId].set_markersize(10)
                self.sensors[sensorId].set_markerfacecolor('g')
            if sensorValue > 0.2:
                self.sensors[sensorId].set_markersize(20)
                self.sensors[sensorId].set_markerfacecolor('b')
            if sensorValue > 0.4:
                self.sensors[sensorId].set_markersize(40)
                self.sensors[sensorId].set_markerfacecolor('#FF5733')
            if sensorValue > 0.6:
                self.sensors[sensorId].set_markersize(60)
                self.sensors[sensorId].set_markerfacecolor('r')


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