import tkinter as tk
import numpy as np
from tkinter import Widget, ttk
from typing import final
from Room import Room
from Sensor import Sensor
from Obstacle import Obstacle
from Program import Program
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import json


#  future plans
# class GuiPage(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        btnCreateRoom = ttk.Button(self, text="Create room", command=lambda: self.controller.show_frame(EditRoomPage))
        btnCreateRoom.grid(row=0, column=0, padx=5, pady=5)

        self.roomFrames = {}
        self.sensorFrames = {}
        self.obstacleFrames = {}
        self.sensorvalues = {}
        self.roomInfoText = {}
        self.sensorInfoTexts = {}
        self.obstacleInfoTexts = {}

        self.roomTabs = ttk.Notebook(self)
        self.loadRooms()

    def reload(self):
        self.roomTabs = ttk.Notebook(self)
        self.loadRooms()

    def loadRooms(self):
        self.controller.program.addRoomsFromNetwork()
        roomsjson = self.controller.program.socketconn.getAllRooms()
        # print("test: " + str(roomsjson))
        rooms = self.controller.program.getRooms()
        # print(roomsjson)
        # print(rooms)
        # print("test: " + str(roomsjson))
        for roomId in rooms:
            self.loadRoom(rooms[roomId])

    def loadRoom(self, room):
        self.roomInfoText[room.id] = {
            "id": tk.StringVar(),
            "name": tk.StringVar(),
            "width": tk.StringVar(),
            "height": tk.StringVar(),
            "length": tk.StringVar(),
        }
        self.roomInfoText[room.id]['id'].set(f"room {str(room.id)}")
        self.sensorFrames[str(room.id)] = {}
        self.obstacleFrames[str(room.id)] = {}
        # future add room check
        self.roomFrames[str(room.id)] = ttk.Frame(self.roomTabs)
        self.roomTabs.add(self.roomFrames[str(room.id)], text=f"room {room.id}")
        self.roomTabs.grid(row=1, column=0, sticky="nsew")

        # legend Frame
        frmLegend = ttk.Frame(self.roomFrames[str(room.id)])
        lblLegend = ttk.Label(frmLegend, text="Legend")

        lblLegend.grid(row=0, column=0, padx=5, pady=5)

        frmLegend.grid(row=0, column=0, padx=5, pady=5)
        # Room info frame
        frmRoomInfo = ttk.Frame(self.roomFrames[str(room.id)])
        lblRoomInfoName = ttk.Label(frmRoomInfo, textvariable=self.roomInfoText[room.id]['id'])

        l, w, h = room.getDimensions()
        roomInfo = {
            "id": room.id,
            "name": room.name,
            "width": w,
            "height": h,
            "length": l,
        }

        btnEditRoom = ttk.Button(frmRoomInfo, text="Edit room",
                                 command=lambda: self.controller.show_frame(EditRoomPage, roomInfo))

        btnEditRoom.grid(row=1, column=0, padx=5, pady=5)

        lblRoomInfoName.grid(row=0, column=0, padx=5, pady=5)

        frmRoomInfo.grid(row=0, column=1, padx=5, pady=5)

        # Sensor add button
        frmSensorAdd = ttk.Frame(self.roomFrames[str(room.id)])
        btnAddSensor = ttk.Button(frmSensorAdd, text="Add Sensor",
                                    command=lambda: self.loadSensorEditPage(room, Sensor(None, None, 0, 0, 0)))
        btnAddSensor.pack(side=tk.LEFT)
        frmSensorAdd.grid(row=1, column=0, padx=5, pady=5)

        #Obstacle add button
        frmObstacleAdd = ttk.Frame(self.roomFrames[str(room.id)])
        btnAddObstacle = ttk.Button(frmObstacleAdd, text="Add Obstacle", 
                                    command=lambda: self.loadObstacleEditPage(room, Obstacle(None, None, 0, 0, 0, 0, 0, 0)))
        btnAddObstacle.pack(side=tk.LEFT)
        frmObstacleAdd.grid(row=1, column=1, padx=5, pady=5)

        #Obstacle list
        frmObstacleList = ttk.Frame(self.roomFrames[str(room.id)])
        canvasObstacleList = tk.Canvas(frmObstacleList)
        scrollbarObstacleList = ttk.Scrollbar(frmObstacleList, orient="vertical", command=canvasObstacleList.yview)
        self.scrollable_frame = ttk.Frame(canvasObstacleList)
        canvasObstacleList.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvasObstacleList.configure(yscrollcommand=scrollbarObstacleList.set)
        
        canvasObstacleList.bind("<Configure>", 
                              lambda e: canvasObstacleList.configure(scrollregion = canvasObstacleList.bbox("all") ))

        for index, obstacle in enumerate(room.getObstacles()):
            self.loadObstacle(obstacle, room, index)

        canvasObstacleList.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbarObstacleList.pack(side=tk.RIGHT, fill="y")

        frmObstacleList.grid(row=2, column=1, padx=5, pady=5)

        # sensor list
        frmSensorList = ttk.Frame(self.roomFrames[str(room.id)])
        canvasSensorList = tk.Canvas(frmSensorList)
        scrollbarSensorList = ttk.Scrollbar(frmSensorList, orient="vertical", command=canvasSensorList.yview)
        self.scrollable_frame = ttk.Frame(canvasSensorList)
        canvasSensorList.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvasSensorList.configure(yscrollcommand=scrollbarSensorList.set)

        canvasSensorList.bind("<Configure>",
                              lambda e: canvasSensorList.configure(scrollregion=canvasSensorList.bbox("all")))

        for index, sensor in enumerate(room.getSensors()):
            self.loadSensor(sensor, room, index)

        canvasSensorList.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbarSensorList.pack(side=tk.RIGHT, fill="y")

        frmSensorList.grid(row=2, column=0, padx=5, pady=5)

        # 3d vieuw
        frm3Dview = ttk.Frame(self.roomFrames[str(room.id)])
        def cuboid_data(o, size=(1,1,1)):
            # print(size)
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

        def plotCubeAt(pos=(0,0,0), size=(1,1,1), ax=None,**kwargs):
            # Plotting a cube element at position pos
            if ax !=None:
                X, Y, Z = cuboid_data( pos, size )
                ax.plot_surface(X, Y, Z, rstride=1, cstride=1, **kwargs)


        fig = Figure(facecolor='xkcd:brown', dpi=100)

        canvas = FigureCanvasTkAgg(fig, master=frm3Dview)
        canvas.draw()

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
            ax.plot(x2, y2, z2, 'or')
            ax.plot(x2, y2, z2, 'or', markersize=50, alpha=0.15)
            for x in range(5):
                ax.plot(x2 + ms * x, y2 + ms * x, z2 + ms * x, 'o', markersize=ms, alpha=0.15)
                ax.plot(x2 + ms * x, y2 - ms * x, z2, 'o', markersize=ms, alpha=0.15)
                ax.plot(x2 - ms * x, y2, z2, 'o', markersize=ms, alpha=0.15)
                ax.plot(x2, y2 - ms * x, z2 + ms * x, 'o', markersize=ms, alpha=0.15)
                ax.plot(x2, y2, z2 - ms * x, 'o', markersize=ms, alpha=0.15)
        
        for i in listObstacles:
            t3 = i.getLocation()
            x3, y3, z3, x4, y4, z4 = t3
            positions = (x3,y3,z3)
            sizes = (x4,y4,z4)
            plotCubeAt(pos=positions, size=sizes, ax=ax)

        toolbar = NavigationToolbar2Tk(canvas, frm3Dview)
        toolbar.update()

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        frm3Dview.grid(row=2, column=3, padx=5, pady=5)

    def loadSensor(self, sensor, room, position):
        self.sensorFrames[str(room.id)][str(sensor.id)] = ttk.Frame(self.scrollable_frame, width=100, height=10,
                                                                    relief=tk.GROOVE, borderwidth=5)
        text = tk.StringVar()
        sensorInfo = {
            'id': tk.StringVar(),
            'name': tk.StringVar()

        }
        text.set(f"value: {sensor.value}")
        sensorInfo['name'].set(sensor.name)
        lblSensorName = ttk.Label(self.sensorFrames[str(room.id)][str(sensor.id)], textvariable=sensorInfo['name'])
        lblSensorValue = ttk.Label(self.sensorFrames[str(room.id)][str(sensor.id)], textvariable=text)
        btnEditSensor = ttk.Button(self.sensorFrames[str(room.id)][str(sensor.id)], text="Edit",
                                   command=lambda: self.loadSensorEditPage(room, sensor))

        # print("Sensor id", sensor.id, "| Sensor value:", sensor.value)
        self.sensorFrames[str(room.id)][str(sensor.id)].grid(row=position, column=0, sticky="nsew")

        lblSensorName.grid(row=0, column=0)
        lblSensorValue.grid(row=0, column=1)
        btnEditSensor.grid(row=0, column=2)
        self.sensorvalues[str(sensor.id)] = text
        self.sensorInfoTexts[sensor.id] = sensorInfo

    def loadObstacle(self, obstacle, room, position):
        obstacleInfo = {
            'name': tk.StringVar() 
        }
        obstacleInfo['name'].set(obstacle.name)
        self.obstacleFrames[str(room.id)][str(obstacle.id)] = ttk.Frame(self.scrollable_frame, width=100, height=10, relief=tk.GROOVE, borderwidth=5)

        lblObstacleName = ttk.Label(self.obstacleFrames[str(room.id)][str(obstacle.id)], textvariable=obstacleInfo['name'])
        btnEditObstacle = ttk.Button(self.obstacleFrames[str(room.id)][str(obstacle.id)], text="Edit", command=lambda: self.loadObstacleEditPage(room, obstacle))

        # print("Obstacle id",obstacle.id,"| Obstacle value:",obstacle.value)
        self.obstacleFrames[str(room.id)][str(obstacle.id)].grid(row=position, column=0, sticky="nsew")

        lblObstacleName.grid(row=0, column=0)
        btnEditObstacle.grid(row=0, column=2)

        self.obstacleInfoTexts[obstacle.id] = obstacleInfo

    def post(self, data):
        pass

    def loadSensorEditPage(self, room, sensor):
        self.controller.setValue([str(room.id), sensor])
        info = {
            'sensor': sensor,
            'room': room
        }
        self.controller.show_frame(EditSensorPage, info)

    def loadObstacleEditPage(self, room, obstacle):
        self.controller.setValue([str(room.id), obstacle])
        info = {
            'obstacle': obstacle,
            'room': room
        }
        self.controller.show_frame(EditObstaclePage, info)

    def updateSensorValue(self, sensorId, sensorValue):
        self.sensorvalues[str(sensorId)].set(sensorValue)
    
    def updateRoom(self, roomId, roomInfo):
        # print(roomId)
        self.roomInfoText[roomId]['id'].set(f"room {str(roomInfo['id'])}")
        self.updateSensors(roomId) #when the rooms get updated the sensors goes as well.
        self.updateObstacles(roomId)
    
    def updateSensors(self, roomId):
        room = self.controller.program.getRoom(roomId)
        for index, sensor in enumerate(room.getSensors()):
            if sensor.getId() in self.sensorInfoTexts:
                self.updateSensor(sensor)
            else:
                self.loadSensor(sensor, room, index)
    
    def updateSensor(self, sensor):
        sensorId = sensor.getId()
        self.sensorInfoTexts[sensorId]['name'].set(sensor.getName())
    
    def updateObstacles(self, roomId):
        room = self.controller.program.getRoom(roomId)
        for index, obstacle in enumerate(room.getObstacles()):
            if obstacle.getId() in self.obstacleInfoTexts:
                self.updateObstacle(obstacle)
            else:
                self.loadObstacle(obstacle, room, index)
    
    def updateObstacle(self, obstacle):
        obstacleId = obstacle.getId()
        self.obstacleInfoTexts[obstacleId]['name'].set(obstacle.getName())
            

class EditRoomPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.id = 0
        self.create = True

        # Name
        frmEditRoomName = ttk.Frame(self)
        lblEditRoomName = ttk.Label(frmEditRoomName, text="Name: ")
        self.entEditRoomName = ttk.Entry(frmEditRoomName)
        lblEditRoomName.grid(row=0, column=0, padx=5, pady=5)
        self.entEditRoomName.grid(row=0, column=1, padx=5, pady=5)
        frmEditRoomName.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # dimensions
        frmEditDimensions = ttk.Frame(self)
        lblEditRoomWidth = ttk.Label(frmEditDimensions, text="Width: ")
        self.entEditRoomWidth = ttk.Entry(frmEditDimensions)
        lblEditRoomWidth.grid(row=0, column=0, padx=5, pady=5, )
        self.entEditRoomWidth.grid(row=0, column=1, padx=5, pady=5)
        lblEditRoomLength = ttk.Label(frmEditDimensions, text="Length: ")
        self.entEditRoomLength = ttk.Entry(frmEditDimensions)
        lblEditRoomLength.grid(row=1, column=0, padx=5, pady=5)
        self.entEditRoomLength.grid(row=1, column=1, padx=5, pady=5)
        lblEditRoomHeight = ttk.Label(frmEditDimensions, text="Height: ")
        self.entEditRoomHeight = ttk.Entry(frmEditDimensions)
        lblEditRoomHeight.grid(row=2, column=0, padx=5, pady=5)
        self.entEditRoomHeight.grid(row=2, column=1, padx=5, pady=5)
        frmEditDimensions.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # save and discard buttons
        frmEditSaveOrDiscard = ttk.Frame(self)
        btnEditRoomSave = ttk.Button(frmEditSaveOrDiscard, text="Save and Exit",
                                     command=lambda: EditRoomPage.saveAndExit(self, controller))
        btnEditRoomSave.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        btnEditRoomDiscard = ttk.Button(frmEditSaveOrDiscard, text="Discard and Exit",
                                        command=lambda: EditRoomPage.discardAndExit(self, controller))
        btnEditRoomDiscard.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        frmEditSaveOrDiscard.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # 3D view

        self.load3dview()
        self.entEditRoomWidth.bind('<KeyRelease>', self.updateAxisEvent)
        self.entEditRoomLength.bind('<KeyRelease>', self.updateAxisEvent)
        self.entEditRoomHeight.bind('<KeyRelease>', self.updateAxisEvent)

    def getInput(self):
        roomInput = {
            'roomName': self.entEditRoomName.get(),
            'width': self.entEditRoomWidth.get(),
            'length': self.entEditRoomLength.get(),
            'height': self.entEditRoomHeight.get()
        }
        return roomInput

    def saveAndExit(self, controller):
        roomName = self.entEditRoomName.get()
        roomX = self.entEditRoomWidth.get()
        roomZ = self.entEditRoomLength.get()
        roomY = self.entEditRoomHeight.get()
        # print(roomName)
        # debugging^
        self.entEditRoomName.delete(0, tk.END)
        self.entEditRoomWidth.delete(0, tk.END)
        self.entEditRoomLength.delete(0, tk.END)
        self.entEditRoomHeight.delete(0, tk.END)

        if (self.create):
            controller.program.createRoom(roomName, roomX, roomY, roomZ)
        else:
            controller.program.editRoom(self.id, roomName, roomX, roomY, roomZ)
        self.create = True

        controller.show_frame(StartPage)

    def discardAndExit(self, controller):
        self.entEditRoomName.delete(0, tk.END)
        self.entEditRoomWidth.delete(0, tk.END)
        self.entEditRoomLength.delete(0, tk.END)
        self.entEditRoomHeight.delete(0, tk.END)
        controller.show_frame(StartPage)

    def post(self, data):
        self.id = data['id']
        self.create = False
        self.entEditRoomName.insert(0, data['name'])
        self.entEditRoomWidth.insert(0, data['width'])
        self.entEditRoomLength.insert(0, data['length'])
        self.entEditRoomHeight.insert(0, data['height'])
        self.updateAxis(data['width'], data['length'], data['height'])

    def load3dview(self):

        # 3D view
        frm3Dview = ttk.Frame(self)

        fig = Figure(facecolor='xkcd:grey', dpi=100)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frm3Dview)
        canvas.draw()

        self.ax = fig.add_subplot(111, projection='3d')

        self.ax.grid(True)
        self.ax.set_facecolor('xkcd:grey')
        self.updateAxis(1, 1, 1)

        frm3Dview.grid(row=1, column=1, padx=5, pady=5)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def updateAxis(self, width, length, height):
        self.ax.set_xlim([0, width])
        self.ax.set_ylim([0, length])
        self.ax.set_zlim([0, height])
        self.ax.set_box_aspect(aspect=(width, length, height))

    # this exists because the event handeler requires that the event parameter exists
    def updateAxisEvent(self, event):
        roomInput = self.getInput()
        if (roomInput['width'].isnumeric() and roomInput['length'].isnumeric() and roomInput['height'].isnumeric()):
            self.updateAxis(float(roomInput['width']), float(roomInput['length']), float(roomInput['height']))
        else:
            self.updateAxis(1, 1, 1)


class EditSensorPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.room = None

        # dimensions
        frmEditLocation = ttk.Frame(self)

        lblEditSensorName = ttk.Label(frmEditLocation, text="Name: ")
        self.entEditSensorName = ttk.Entry(frmEditLocation)
        lblEditSensorName.grid(row=0, column=0, padx=5, pady=5, )
        self.entEditSensorName.grid(row=0, column=1, padx=5, pady=5)

        lblEditSensorX = ttk.Label(frmEditLocation, text="X: ")
        self.entEditSensorX = ttk.Entry(frmEditLocation)
        lblEditSensorX.grid(row=1, column=0, padx=5, pady=5, )
        self.entEditSensorX.grid(row=1, column=1, padx=5, pady=5)

        lblEditSensorY = ttk.Label(frmEditLocation, text="Y: ")
        self.entEditSensorY = ttk.Entry(frmEditLocation)
        lblEditSensorY.grid(row=2, column=0, padx=5, pady=5)
        self.entEditSensorY.grid(row=2, column=1, padx=5, pady=5)

        lblEditSensorZ = ttk.Label(frmEditLocation, text="Z: ")
        self.entEditSensorZ = ttk.Entry(frmEditLocation)
        lblEditSensorZ.grid(row=3, column=0, padx=5, pady=5)
        self.entEditSensorZ.grid(row=3, column=1, padx=5, pady=5)

        frmEditLocation.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # save and discard buttons
        frmEditSensorSaveOrDiscard = ttk.Frame(self)
        btnEditSensorSave = ttk.Button(frmEditSensorSaveOrDiscard, text="Save and Exit",
                                       command=lambda: EditSensorPage.saveAndExit(self, controller))
        btnEditSensorSave.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        btnEditSensorDiscard = ttk.Button(frmEditSensorSaveOrDiscard, text="Discard and Exit",
                                          command=lambda: EditSensorPage.discardAndExit(self, controller))
        btnEditSensorDiscard.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        frmEditSensorSaveOrDiscard.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.load3dview()

        self.entEditSensorX.bind('<KeyRelease>', self.plotSensorEvent)
        self.entEditSensorY.bind('<KeyRelease>', self.plotSensorEvent)
        self.entEditSensorZ.bind('<KeyRelease>', self.plotSensorEvent)

    def load3dview(self):

        SensorX = 0
        SensorY = 0
        SensorZ = 0

        # 3D view
        frm3Dview = ttk.Frame(self)

        fig = Figure(facecolor='xkcd:grey', dpi=100)

        canvas = FigureCanvasTkAgg(fig, master=frm3Dview)
        canvas.draw()

        self.ax = fig.add_subplot(111, projection='3d')

        self.ax.grid(True)
        self.ax.set_facecolor('xkcd:grey')
        self.setRoomAxis()

        self.plotSensor(SensorX, SensorY, SensorZ)

        frm3Dview.grid(row=1, column=1, padx=5, pady=5)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def setRoomAxis(self):
        if (self.room == None):
            x1, y1, z1 = (500, 500, 500)
        else:
            x1, y1, z1 = self.room.getDimensions()
        self.ax.set_xlim([0, x1])
        self.ax.set_ylim([0, y1])
        self.ax.set_zlim([0, z1])
        self.ax.set_box_aspect(aspect=(x1, y1, z1))

    def plotSensor(self, x, y, z):
        self.ax.clear()
        self.setRoomAxis()
        plot = self.ax.plot(x, y, z, 'ro')

    def plotSensorEvent(self, event):
        sensorInput = self.getInput()
        if (sensorInput['x'].isnumeric() and sensorInput['y'].isnumeric() and sensorInput['z'].isnumeric()):
            self.plotSensor(float(sensorInput['x']), float(sensorInput['y']), float(sensorInput['z']))
        else:
            self.plotSensor(1, 1, 1)

    def getInput(self):
        sensorInfo = {
            'name': self.entEditSensorName.get(),
            'x': self.entEditSensorX.get(),
            'y': self.entEditSensorY.get(),
            'z': self.entEditSensorZ.get()
        }
        return sensorInfo

    def insert(self, sensor):
        self.entEditSensorName.insert(0, sensor.name)

    def saveAndExit(self, controller):
        name = self.entEditSensorName.get()
        sensorX = self.entEditSensorX.get()
        sensorY = self.entEditSensorY.get()
        sensorZ = self.entEditSensorZ.get()

        self.entEditSensorName.delete(0, tk.END)
        self.entEditSensorX.delete(0, tk.END)
        self.entEditSensorY.delete(0, tk.END)
        self.entEditSensorZ.delete(0, tk.END)

        # print(controller.getValue()[1].id)
        if (controller.getValue()[1].id != None):
            controller.program.editSensor(controller.getValue()[1].id, name, sensorX, sensorY, sensorZ)
        else:
            controller.program.addSensor(controller.getValue()[0], name, sensorX, sensorY, sensorZ)
        controller.show_frame(StartPage)

    def discardAndExit(self, controller):
        self.entEditSensorName.delete(0, tk.END)
        self.entEditSensorX.delete(0, tk.END)
        self.entEditSensorY.delete(0, tk.END)
        self.entEditSensorZ.delete(0, tk.END)
        controller.show_frame(StartPage)

    def post(self, info):
        self.room = info['room']
        self.plotSensor(info['sensor'].x, info['sensor'].y, info['sensor'].z)
        if (info['sensor'].name != None):
            self.entEditSensorName.insert(0, info['sensor'].name)
            self.entEditSensorX.insert(0, info['sensor'].x)
            self.entEditSensorY.insert(0, info['sensor'].y)
            self.entEditSensorZ.insert(0, info['sensor'].z)
        pass

class EditObstaclePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #dimensions
        frmEditLocation = ttk.Frame(self)

        lblEditObstacleName = ttk.Label(frmEditLocation, text="Name: ")
        self.entEditObstacleName = ttk.Entry(frmEditLocation)
        lblEditObstacleName.grid(row=0, column=0, padx=5, pady=5,)
        self.entEditObstacleName.grid(row=0, column=1, padx=5, pady=5)

        lblEditObstacleX1 = ttk.Label(frmEditLocation, text="X1: ")
        self.entEditObstacleX1 = ttk.Entry(frmEditLocation)
        lblEditObstacleX1.grid(row=1, column=0, padx=5, pady=5,)
        self.entEditObstacleX1.grid(row=1, column=1, padx=5, pady=5)

        lblEditObstacleY1 = ttk.Label(frmEditLocation, text="Y1: ")
        self.entEditObstacleY1 = ttk.Entry(frmEditLocation)
        lblEditObstacleY1.grid(row=2, column=0, padx=5, pady=5,)
        self.entEditObstacleY1.grid(row=2, column=1, padx=5, pady=5)

        lblEditObstacleZ1 = ttk.Label(frmEditLocation, text="Z1: ")
        self.entEditObstacleZ1 = ttk.Entry(frmEditLocation)
        lblEditObstacleZ1.grid(row=3, column=0, padx=5, pady=5,)
        self.entEditObstacleZ1.grid(row=3, column=1, padx=5, pady=5)

        lblEditObstacleX2 = ttk.Label(frmEditLocation, text="X2: ")
        self.entEditObstacleX2 = ttk.Entry(frmEditLocation)
        lblEditObstacleX2.grid(row=4, column=0, padx=5, pady=5,)
        self.entEditObstacleX2.grid(row=4, column=1, padx=5, pady=5)

        lblEditObstacleY2 = ttk.Label(frmEditLocation, text="Y2: ")
        self.entEditObstacleY2 = ttk.Entry(frmEditLocation)
        lblEditObstacleY2.grid(row=5, column=0, padx=5, pady=5,)
        self.entEditObstacleY2.grid(row=5, column=1, padx=5, pady=5)

        lblEditObstacleZ2 = ttk.Label(frmEditLocation, text="Z2: ")
        self.entEditObstacleZ2 = ttk.Entry(frmEditLocation)
        lblEditObstacleZ2.grid(row=6, column=0, padx=5, pady=5,)
        self.entEditObstacleZ2.grid(row=6, column=1, padx=5, pady=5)

        frmEditLocation.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        #save and discard buttons
        frmEditObstacleSaveOrDiscard = ttk.Frame(self)
        btnEditObstacleSave = ttk.Button(frmEditObstacleSaveOrDiscard, text="Save and Exit", command=lambda: EditObstaclePage.saveAndExit(self, controller))
        btnEditObstacleSave.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        btnEditObstacleDiscard = ttk.Button(frmEditObstacleSaveOrDiscard, text="Discard and Exit", command=lambda: EditObstaclePage.discardAndExit(self, controller))
        btnEditObstacleDiscard.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        frmEditObstacleSaveOrDiscard.grid(row=2, column=0, padx=5, pady=5, sticky="w")


    def insert(self, obstacle):
        self.entEditObstacleName.insert(0, obstacle.name)
    
    def saveAndExit(self, controller):
        name = self.entEditObstacleName.get()
        obstacleX1 = self.entEditObstacleX1.get()
        obstacleY1 = self.entEditObstacleY1.get()
        obstacleZ1 = self.entEditObstacleZ1.get()
        obstacleX2 = self.entEditObstacleX2.get()
        obstacleY2 = self.entEditObstacleY2.get()
        obstacleZ2 = self.entEditObstacleZ2.get()

        self.entEditObstacleName.delete(0, tk.END)
        self.entEditObstacleX1.delete(0, tk.END)
        self.entEditObstacleY1.delete(0, tk.END)
        self.entEditObstacleZ1.delete(0, tk.END)
        self.entEditObstacleX2.delete(0, tk.END)
        self.entEditObstacleY2.delete(0, tk.END)
        self.entEditObstacleZ2.delete(0, tk.END)

        # print(controller.getValue()[1].id)
        if(controller.getValue()[1].id != None):
            controller.program.editObstacle(controller.getValue()[1].id, name, obstacleX1, obstacleY1, obstacleZ1, obstacleX2, obstacleY2, obstacleZ2)
        else:
            controller.program.addObstacle(controller.getValue()[0], name, obstacleX1, obstacleY1, obstacleZ1, obstacleX2, obstacleY2, obstacleZ2)
        controller.show_frame(StartPage)

        
    def discardAndExit(self, controller):
        self.entEditObstacleName.delete(0, tk.END)
        self.entEditObstacleX1.delete(0, tk.END)
        self.entEditObstacleY1.delete(0, tk.END)
        self.entEditObstacleZ1.delete(0, tk.END)
        self.entEditObstacleX2.delete(0, tk.END)
        self.entEditObstacleY2.delete(0, tk.END)
        self.entEditObstacleZ2.delete(0, tk.END)
        controller.show_frame(StartPage)

    def post(self, info):
        self.room = info['room']

        if(info['obstacle'].name != None):
            self.entEditObstacleName.insert(0, info['obstacle'].name)
            self.entEditObstacleX1.insert(0, info['obstacle'].x1)
            self.entEditObstacleY1.insert(0, info['obstacle'].y1)
            self.entEditObstacleZ1.insert(0, info['obstacle'].z1)
            self.entEditObstacleX2.insert(0, info['obstacle'].x2)
            self.entEditObstacleY2.insert(0, info['obstacle'].y2)
            self.entEditObstacleZ2.insert(0, info['obstacle'].z2)
        pass
