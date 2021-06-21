import tkinter as tk
import numpy as np
from tkinter import Widget, ttk
from typing import final
from Room import Room
from Sensor import Sensor
from Obstacle import Obstacle
from Program import Program
from Visualization import Visualization
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
plt.style.use('seaborn-white')

#  future plans
# class GuiPage(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)

class StartPage(tk.Frame):

    currentView = np.array([], np.int)
    view = np.array([], np.int)
    zLayer = np.array([])
    pValue = np.array([])

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        btnCreateRoom = ttk.Button(self, text="Create room", command=lambda: self.controller.show_frame(EditRoomPage))
        btnCreateRoom.grid(row=0, column=0, padx=5, pady=5)

        self.roomFrames = {}
        self.sensorFrames = {}
        self.obstacleFrames = {}

        self.roomTabs = ttk.Notebook(self)
        self.loadRooms()

    def reload(self):
        self.roomTabs = ttk.Notebook(self)
        self.loadRooms()

    def loadRooms(self):
        self.controller.program.addRoomsFromNetwork()
        rooms = self.controller.program.getRooms()
        
        for room in rooms:
            #print(room.id-1)
            self.currentView = np.append(self.currentView, 1)
            self.view = np.append(self.view, 0)
            self.zLayer = np.append(self.zLayer, 0)
            self.pValue = np.append(self.pValue, 2)
            self.loadRoom(room)
        

    def loadRoom(self, room):
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
        lblRoomInfoName = ttk.Label(frmRoomInfo, text=f"room {str(room.id)}")

        l, w, h = room.getDimensions()

        roomInfo = {
            "id": room.id,
            "name": room.name,
            "width": w,
            "height": h,
            "length": l,
        }
        btnReload = ttk.Button(self, text="reload", command=lambda: self.reload())
        btnReload.grid(row=0, column=1, padx=5, pady=5)

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

        #Change view button
        frmViewChange = ttk.Frame(self.roomFrames[str(room.id)])
        btnChangeView = ttk.Button(frmViewChange, text="2D <-> 3D",
                                    command=lambda: changeView())
        btnChangeView.pack(fill=tk.Y, side=tk.LEFT)
        frmViewChange.grid(row=1, column=3, padx=5, pady=5)

        btnTop = ttk.Button(frmViewChange, text="Top",
                                   command=lambda: view(0))
        btnTop.pack(fill=tk.Y, side=tk.LEFT)

        btnLeft = ttk.Button(frmViewChange, text="Left",
                                    command=lambda: view(1))
        btnLeft.pack(fill=tk.Y, side=tk.LEFT)

        btnRight = ttk.Button(frmViewChange, text="Right",
                                    command=lambda: view(2))
        btnRight.pack(fill=tk.Y, side=tk.LEFT)

        #Layer of unseen dimension in 2d, i.e. length and width are seen, z is wich layer in depth is to be shown
        lblEditLayer = ttk.Label(frmViewChange, text="Layer:")
        lblEditLayer.pack(fill=tk.Y, side=tk.LEFT)
        zEntry = ttk.Entry(frmViewChange, width=3)
        zEntry.pack(fill=tk.Y, side=tk.LEFT)
        zEntry.insert(0, self.zLayer[room.id-1])

        #variable for inverse distance weighting
        lblEditP = ttk.Label(frmViewChange, text="P:")
        lblEditP.pack(fill=tk.Y, side=tk.LEFT)
        pEntry = ttk.Entry(frmViewChange, width=3)
        pEntry.pack(fill=tk.Y, side=tk.LEFT)
        pEntry.insert(0, self.pValue[room.id-1])

        visual = Visualization()
              
        def view(side):
            self.currentView[room.id-1] = 0
            self.view[room.id-1] = side
            show2D()

        def changeView():
            #print("room: " + str(room.id-1))
            #print("view: " + str(self.currentView[room.id-1]))
            if self.currentView[room.id-1] == 0:
                self.currentView[room.id-1] = 1
                frm3Dview = ttk.Frame(self.roomFrames[str(room.id)])
                canvas = FigureCanvasTkAgg(visual.view3D(room), master=frm3Dview)
                canvas.draw()

                toolbar = NavigationToolbar2Tk(canvas, frm3Dview)
                toolbar.update()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                frm3Dview.grid(row=2, column=3, padx=5, pady=5)

            else:
                self.currentView[room.id-1] = 0
                show2D()
                
        def show2D():
            self.zLayer[room.id-1] = zEntry.get()
            self.pValue[room.id-1] = pEntry.get()
            frm2Dview = ttk.Frame(self.roomFrames[str(room.id)])
                
            canvas = FigureCanvasTkAgg(visual.view2D(room, self.zLayer[room.id-1], self.pValue[room.id-1], self.view[room.id-1]), master=frm2Dview)
            canvas.draw()

            toolbar = NavigationToolbar2Tk(canvas, frm2Dview)
            toolbar.update()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            frm2Dview.grid(row=2, column=3, padx=5, pady=5)

            
        changeView()
        

    

    def loadSensor(self, sensor, room, position):
        self.sensorFrames[str(room.id)][str(sensor.id)] = ttk.Frame(self.scrollable_frame, width=100, height=10,
                                                                    relief=tk.GROOVE, borderwidth=5)

        lblSensorName = ttk.Label(self.sensorFrames[str(room.id)][str(sensor.id)], text=sensor.name)
        lblSensorValue = ttk.Label(self.sensorFrames[str(room.id)][str(sensor.id)], text=f"value: {sensor.value}")
        btnEditSensor = ttk.Button(self.sensorFrames[str(room.id)][str(sensor.id)], text="Edit",
                                   command=lambda: self.loadSensorEditPage(room, sensor))

        #print("Sensor id", sensor.id, "| Sensor value:", sensor.value)
        self.sensorFrames[str(room.id)][str(sensor.id)].grid(row=position, column=0, sticky="nsew")

        lblSensorName.grid(row=0, column=0)
        lblSensorValue.grid(row=0, column=1)
        btnEditSensor.grid(row=0, column=2)

    def loadObstacle(self, obstacle, room, position):
        self.obstacleFrames[str(room.id)][str(obstacle.id)] = ttk.Frame(self.scrollable_frame, width=100, height=10, relief=tk.GROOVE, borderwidth=5)

        lblObstacleName = ttk.Label(self.obstacleFrames[str(room.id)][str(obstacle.id)], text=obstacle.name)
        btnEditObstacle = ttk.Button(self.obstacleFrames[str(room.id)][str(obstacle.id)], text="Edit", command=lambda: self.loadObstacleEditPage(room, obstacle))

        #print("Obstacle id",obstacle.id,"| Obstacle value:",obstacle.value)
        self.obstacleFrames[str(room.id)][str(obstacle.id)].grid(row=position, column=0, sticky="nsew")

        lblObstacleName.grid(row=0, column=0)
        btnEditObstacle.grid(row=0, column=2)

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
        #print(roomName)
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

        #print(controller.getValue()[1].id)
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

        #print(controller.getValue()[1].id)
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
