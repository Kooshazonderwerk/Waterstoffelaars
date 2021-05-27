import tkinter as tk
from tkinter import Widget, ttk
from typing import final
from Room import Room
from Sensor import Sensor
from Program import Program
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

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

        self.roomTabs = ttk.Notebook(self)
        self.loadRooms()

    def reload(self):
        self.roomTabs = ttk.Notebook(self)
        self.loadRooms()

    def loadRooms(self): 
        self.controller.program.addRoomsFromNetwork()
        rooms = self.controller.program.getRooms()
        for room in rooms:
            self.loadRoom(room)

    def loadRoom(self, room):
        self.sensorFrames[str(room.id)] = {}
        # future add room check
        self.roomFrames[str(room.id)] = ttk.Frame(self.roomTabs)
        self.roomTabs.add(self.roomFrames[str(room.id)], text=f"room {room.id}")
        self.roomTabs.grid(row=1, column=0, sticky="nsew")

        #legend Frame
        frmLegend = ttk.Frame(self.roomFrames[str(room.id)])
        lblLegend = ttk.Label(frmLegend, text="Legend")

        lblLegend.grid(row=0, column=0, padx=5, pady=5)

        frmLegend.grid(row=0, column=0, padx=5, pady=5)
        #Room info frame
        frmRoomInfo = ttk.Frame(self.roomFrames[str(room.id)])
        lblRoomInfoName = ttk.Label(frmRoomInfo, text=f"room {str(room.id)}")

        l, w, h = room.getDimensions()

        roomInfo = {
            "id": room.id,
            "name": room.name,
            "width":w,
            "height":h,
            "length":l,
        }

        btnEditRoom = ttk.Button(frmRoomInfo, text="Edit room", command=lambda: self.controller.show_frame(EditRoomPage, roomInfo))

        btnEditRoom.grid(row=1, column=0, padx=5, pady=5)


        lblRoomInfoName.grid(row=0, column=0, padx=5, pady=5)

        frmRoomInfo.grid(row=0, column=1, padx=5, pady=5)

        #Sensor add button
        frmSensorAdd = ttk.Frame(self.roomFrames[str(room.id)])
        btnAddSensor = ttk.Button(frmSensorAdd, text="Add Sensor", command=lambda: self.loadSensorEditPage(room, Sensor(None, None, 0, 0, 0)))
        btnAddSensor.pack(side=tk.LEFT)
        frmSensorAdd.grid(row=1, column=0, padx=5, pady=5)


        #sensor list
        frmSensorList = ttk.Frame(self.roomFrames[str(room.id)])
        canvasSensorList = tk.Canvas(frmSensorList)
        scrollbarSensorList = ttk.Scrollbar(frmSensorList, orient="vertical", command=canvasSensorList.yview)
        self.scrollable_frame = ttk.Frame(canvasSensorList)
        canvasSensorList.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvasSensorList.configure(yscrollcommand=scrollbarSensorList.set)
        
        canvasSensorList.bind("<Configure>", lambda e: canvasSensorList.configure(scrollregion = canvasSensorList.bbox("all") ))

        for index, sensor in enumerate(room.getSensors()):
            self.loadSensor(sensor, room, index)

        canvasSensorList.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbarSensorList.pack(side=tk.RIGHT, fill="y")

        frmSensorList.grid(row=2, column=0, padx=5, pady=5)


        #3d vieuw
        frm3Dview = ttk.Frame(self.roomFrames[str(room.id)])


        fig = Figure(facecolor = 'xkcd:brown', dpi=100)


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
        ax.set_box_aspect(aspect = (x1, y1, z1))

        list = room.getSensors()

        for i in list:
            t2 = i.getLocation()
            x2, y2, z2 = t2
            ax.plot(x2, y2, z2, 'ro')

        toolbar = NavigationToolbar2Tk(canvas, frm3Dview)
        toolbar.update()

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        frm3Dview.grid(row=2, column=1, padx=5, pady=5)

    def loadSensor(self, sensor, room, position):
        self.sensorFrames[str(room.id)][str(sensor.id)] = ttk.Frame(self.scrollable_frame, width=100, height=10, relief=tk.GROOVE, borderwidth=5)

        lblSensorName = ttk.Label(self.sensorFrames[str(room.id)][str(sensor.id)], text=sensor.name)
        lblSensorValue = ttk.Label(self.sensorFrames[str(room.id)][str(sensor.id)], text=f"value: {sensor.value}")
        btnEditSensor = ttk.Button(self.sensorFrames[str(room.id)][str(sensor.id)], text="Edit", command=lambda: self.loadSensorEditPage(room, sensor))

        print("Sensor id",sensor.id,"| Sensor value:",sensor.value)
        self.sensorFrames[str(room.id)][str(sensor.id)].grid(row=position, column=0, sticky="nsew")

        lblSensorName.grid(row=0, column=0)
        lblSensorValue.grid(row=0, column=1)
        btnEditSensor.grid(row=0, column=2)

    def post(self, data):
        pass

    def loadSensorEditPage(self, room, sensor):
        self.controller.setValue([str(room.id), sensor])
        info = {
            'sensor': sensor,
            'room': room
        }
        self.controller.show_frame(EditSensorPage, info)


class EditRoomPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.id = 0
        self.create = True

        #Name
        frmEditRoomName = ttk.Frame(self)
        lblEditRoomName = ttk.Label(frmEditRoomName, text="Name: ")
        self.entEditRoomName = ttk.Entry(frmEditRoomName)
        lblEditRoomName.grid(row=0, column=0, padx=5, pady=5)
        self.entEditRoomName.grid(row=0, column=1, padx=5, pady=5)
        frmEditRoomName.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        #dimensions
        frmEditDimensions = ttk.Frame(self)
        lblEditRoomWidth = ttk.Label(frmEditDimensions, text="Width: ")
        self.entEditRoomWidth = ttk.Entry(frmEditDimensions)
        lblEditRoomWidth.grid(row=0, column=0, padx=5, pady=5,)
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

        #save and discard buttons
        frmEditSaveOrDiscard = ttk.Frame(self)
        btnEditRoomSave = ttk.Button(frmEditSaveOrDiscard, text="Save and Exit", command=lambda: EditRoomPage.saveAndExit(self, controller))
        btnEditRoomSave.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        btnEditRoomDiscard = ttk.Button(frmEditSaveOrDiscard, text="Discard and Exit", command=lambda: EditRoomPage.discardAndExit(self, controller))
        btnEditRoomDiscard.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        frmEditSaveOrDiscard.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        #3D view

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
        print(roomName)
        #debugging^
        self.entEditRoomName.delete(0, tk.END)
        self.entEditRoomWidth.delete(0, tk.END)
        self.entEditRoomLength.delete(0, tk.END)
        self.entEditRoomHeight.delete(0, tk.END)

        if(self.create):
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


        #3D view
        frm3Dview = ttk.Frame(self)

        fig = Figure(facecolor = 'xkcd:grey', dpi=100)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frm3Dview)
        canvas.draw()

        self.ax = fig.add_subplot(111, projection='3d')

        self.ax.grid(True)
        self.ax.set_facecolor('xkcd:grey')
        self.updateAxis(1,1,1)

        frm3Dview.grid(row=1, column=1, padx=5, pady=5)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def updateAxis(self, width, length, height):
        self.ax.set_xlim([0, width])
        self.ax.set_ylim([0, length])
        self.ax.set_zlim([0, height])
        self.ax.set_box_aspect(aspect = (width, length, height))


    #this exists because the event handeler requires that the event parameter exists
    def updateAxisEvent(self, event):
        roomInput = self.getInput()
        if(roomInput['width'].isnumeric() and roomInput['length'].isnumeric() and roomInput['height'].isnumeric()):
            self.updateAxis(float(roomInput['width']), float(roomInput['length']), float(roomInput['height']))
        else:
            self.updateAxis(1,1,1)


class EditSensorPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.room = None

        #dimensions
        frmEditLocation = ttk.Frame(self)

        lblEditSensorName = ttk.Label(frmEditLocation, text="Name: ")
        self.entEditSensorName = ttk.Entry(frmEditLocation)
        lblEditSensorName.grid(row=0, column=0, padx=5, pady=5,)
        self.entEditSensorName.grid(row=0, column=1, padx=5, pady=5)

        lblEditSensorX = ttk.Label(frmEditLocation, text="X: ")
        self.entEditSensorX = ttk.Entry(frmEditLocation)
        lblEditSensorX.grid(row=1, column=0, padx=5, pady=5,)
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

        #save and discard buttons
        frmEditSensorSaveOrDiscard = ttk.Frame(self)
        btnEditSensorSave = ttk.Button(frmEditSensorSaveOrDiscard, text="Save and Exit", command=lambda: EditSensorPage.saveAndExit(self, controller))
        btnEditSensorSave.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        btnEditSensorDiscard = ttk.Button(frmEditSensorSaveOrDiscard, text="Discard and Exit", command=lambda: EditSensorPage.discardAndExit(self, controller))
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

        #3D view
        frm3Dview = ttk.Frame(self)

        fig = Figure(facecolor = 'xkcd:grey', dpi=100)

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
        if(self.room == None):
            x1, y1, z1 = (500,500,500)
        else:
            x1, y1, z1 = self.room.getDimensions()
        self.ax.set_xlim([0, x1])
        self.ax.set_ylim([0, y1])
        self.ax.set_zlim([0, z1])
        self.ax.set_box_aspect(aspect = (x1, y1, z1))

    def plotSensor(self, x, y, z):
        self.ax.clear()
        self.setRoomAxis()
        plot = self.ax.plot(x, y, z, 'ro')
    
    def plotSensorEvent(self, event):
        sensorInput = self.getInput()
        if(sensorInput['x'].isnumeric() and sensorInput['y'].isnumeric() and sensorInput['z'].isnumeric()):
            self.plotSensor(float(sensorInput['x']), float(sensorInput['y']), float(sensorInput['z']))
        else:
            self.plotSensor(1,1,1)

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

        print(controller.getValue()[1].id)
        if(controller.getValue()[1].id != None):
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
        if(info['sensor'].name != None):
            self.entEditSensorName.insert(0, info['sensor'].name)
            self.entEditSensorX.insert(0, info['sensor'].x)
            self.entEditSensorY.insert(0, info['sensor'].y)
            self.entEditSensorZ.insert(0, info['sensor'].z)
        pass
