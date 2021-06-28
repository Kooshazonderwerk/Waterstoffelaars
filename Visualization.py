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
        for sensor in room.getSensors():
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

    def view3D(self, room):
        
        fig = Figure(facecolor='xkcd:brown', dpi=100)

        ax = fig.add_subplot(111, projection='3d')
        fig.tight_layout()
        t1 = room.getDimensions()
        x1, y1, z1 = t1

        ax.grid(False)
        ax.set_facecolor('xkcd:brown')
        ax.set_xlim([0, x1])
        ax.set_ylim([0, y1])
        ax.set_zlim([0, z1])
        ax.set_box_aspect(aspect=(x1, y1, z1))

        list = room.getSensors()
        listObstacles = room.getObstacles()

        for i in list:
            t2 = i.getLocation()
            x2, y2, z2 = t2
            ms = 20  # markersize
            if i.value < 0.1:
                ax.plot(x2, y2, z2, 'o',color='#95A5A6', markersize=5)
            if i.value > 0.1:
                ax.plot(x2, y2, z2, 'o',color='g', markersize=10)
            if i.value > 0.2:
                ax.plot(x2, y2, z2, 'o',color='b',markersize=20)
            if i.value > 0.4:
                ax.plot(x2, y2, z2, 'o',color='#FF5733',markersize=40)
            if i.value > 0.6:
                ax.plot(x2, y2, z2, 'o',color='r',markersize=60)

            # ax.plot(x2, y2, z2, 'or', markersize=50, alpha=0.15)
            # for x in range(5):
            #     ax.plot(x2 + ms * x, y2 + ms * x, z2 + ms * x, 'o', markersize=ms, alpha=0.15)
            #     ax.plot(x2 + ms * x, y2 - ms * x, z2, 'o', markersize=ms, alpha=0.15)
            #     ax.plot(x2 - ms * x, y2, z2, 'o', markersize=ms, alpha=0.15)
            #     ax.plot(x2, y2 - ms * x, z2 + ms * x, 'o', markersize=ms, alpha=0.15)
            #     ax.plot(x2, y2, z2 - ms * x, 'o', markersize=ms, alpha=0.15)
        
        for i in listObstacles:
            t3 = i.getLocation()
            x3, y3, z3, x4, y4, z4 = t3
            positions = (x3,y3,z3)
            sizes = (x4,y4,z4)
            self.plotCubeAt(pos=positions, size=sizes, ax=ax)

        
        return fig

        #wat is dit?
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
            ax.plot_surface(X, Y, Z, rstride=1, cstride=1, **kwargs)