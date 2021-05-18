import tkinter as tk
from tkinter import ttk
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
        btnReload = ttk.Button(self, text="reload", command=lambda: self.reload())
        btnReload.grid(row=0, column=1, padx=5, pady=5)

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

        lblRoomInfoName.grid(row=0, column=0, padx=5, pady=5)

        frmRoomInfo.grid(row=0, column=1, padx=5, pady=5)

        #Sensor add button
        frmSensorAdd = ttk.Frame(self.roomFrames[str(room.id)])
        btnAddSensor = ttk.Button(frmSensorAdd, text="Add Sensor", command=lambda: self.loadSensorEditPage(str(room.id)))
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
            self.loadSensor(sensor, room.id, index)

        canvasSensorList.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbarSensorList.pack(side=tk.RIGHT, fill="y")

        frmSensorList.grid(row=2, column=0, padx=5, pady=5)


        #3d vieuw
        frm3Dview = ttk.Frame(self.roomFrames[str(room.id)])


        fig = Figure(figsize=(5, 4), dpi=100)

        canvas = FigureCanvasTkAgg(fig, master=frm3Dview)
        canvas.draw()

        ax = fig.add_subplot(111, projection='3d')
        t1 = room.getDimensions()
        x1, y1, z1 = t1

        ax.grid(False)
        ax.set_facecolor('xkcd:brown')
        ax.set_xlim([0, x1])
        ax.set_ylim([0, y1])
        ax.set_zlim([0, z1])

        list = enumerate(room.getSensors())
        print(list)
        for i in list:
            t2 = sensor.getLocation()
            x2, y2, z2 = t2
            ax.plot(x2, y2, z2, 'ro')

        toolbar = NavigationToolbar2Tk(canvas, frm3Dview)
        toolbar.update()


        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        frm3Dview.grid(row=2, column=1, padx=5, pady=5)

    def loadSensor(self, sensor, roomid, position):
        self.sensorFrames[str(roomid)][str(sensor.id)] = ttk.Frame(self.scrollable_frame, width=50, height=10, relief=tk.GROOVE, borderwidth=5)

        lblSensorName = ttk.Label(self.sensorFrames[str(roomid)][str(sensor.id)], text=sensor.name)
        lblSensorValue = ttk.Label(self.sensorFrames[str(roomid)][str(sensor.id)], text="value: 0.0")
        btnEditSensor = ttk.Button(self.sensorFrames[str(roomid)][str(sensor.id)], text="Edit", command=lambda: self.loadSensorEditPage(roomid, sensor))
        print(str(sensor.id) + " " + sensor.name)
        
        self.sensorFrames[str(roomid)][str(sensor.id)].grid(row=position, column=0, sticky="nsew")

        lblSensorName.grid(row=0, column=0)
        lblSensorValue.grid(row=0, column=1)
        btnEditSensor.grid(row=0, column=2)
    
    def loadSensorEditPage(self, value, sensor):
        #EditSensorPage.insert(EditSensorPage, sensor)
        self.controller.setValue([value, sensor])
        self.controller.show_frame(EditSensorPage)


class EditRoomPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

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
        controller.program.createRoom(roomName, roomX, roomY, roomZ)
        controller.show_frame(StartPage)

    def discardAndExit(self, controller):
        self.entEditRoomName.delete(0, tk.END)
        self.entEditRoomWidth.delete(0, tk.END)
        self.entEditRoomLength.delete(0, tk.END)
        self.entEditRoomHeight.delete(0, tk.END)
        controller.show_frame(StartPage)

class EditSensorPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

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
        btnEditSensorSave.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        btnEditSensorDiscard = ttk.Button(frmEditSensorSaveOrDiscard, text="Discard and Exit", command=lambda: EditSensorPage.discardAndExit(self, controller))
        btnEditSensorDiscard.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        frmEditSensorSaveOrDiscard.grid(row=2, column=0, padx=5, pady=5, sticky="w")

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
        controller.program.editSensor(controller.getValue()[1].id, name, sensorX, sensorY, sensorZ)
        controller.show_frame(StartPage)
        
    def discardAndExit(self, controller):
        self.entEditSensorName.delete(0, tk.END)
        self.entEditSensorX.delete(0, tk.END)
        self.entEditSensorY.delete(0, tk.END)
        self.entEditSensorZ.delete(0, tk.END)
        controller.show_frame(StartPage)
