import tkinter as tk
from tkinter import ttk
from Room import Room
from Sensor import Sensor
from Program import Program

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

    def loadRooms(self): 
        self.controller.program.addRoomsFromNetwork()
        rooms = self.controller.program.getRooms()
        for room in rooms:
            self.loadRoom(room)

    def loadRoom(self, room):
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
        btnAddSensor = ttk.Button(frmSensorAdd, text="Add Sensor", command=lambda: controller.show_frame(EditSensorPage))
        btnAddSensor.pack(side=tk.LEFT)
        frmSensorAdd.grid(row=1, column=0, padx=5, pady=5)


        #sensor list
        frmSensorList = ttk.Frame(self.roomFrames[str(room.id)])
        canvasSensorList = tk.Canvas(frmSensorList)
        scrollbarSensorList = ttk.Scrollbar(frmSensorList, orient="vertical", command=canvasSensorList.yview)
        scrollable_frame = ttk.Frame(canvasSensorList)
        canvasSensorList.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvasSensorList.configure(yscrollcommand=scrollbarSensorList.set)
        
        canvasSensorList.bind("<Configure>", lambda e: canvasSensorList.configure(scrollregion = canvasSensorList.bbox("all") ))

        for index, sensor in enumerate(room.getSensors()):
            self.loadSensor(sensor, index, scrollable_frame)

        canvasSensorList.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbarSensorList.pack(side=tk.RIGHT, fill="y")

        frmSensorList.grid(row=2, column=0, padx=5, pady=5)


        #3d vieuw placeholder
        frm3Dview = ttk.Frame(self.roomFrames[str(room.id)])
        lbl3DTemp = ttk.Label(frm3Dview, font=('Helvetica', 30), text="3d placeholder")
        lbl3DTemp.pack(fill=tk.BOTH)
        frm3Dview.grid(row=2, column=1, padx=5, pady=5)

    def loadSensor(self, sensor, position, scrollable_frame):
        frmSensorInfo = ttk.Frame(scrollable_frame, width=50, height=10, relief=tk.GROOVE, borderwidth=5)

        lblSensorName = ttk.Label(frmSensorInfo, text=f"Sensor id: {sensor.id}")
        lblSensorValue = ttk.Label(frmSensorInfo, text="value: 0.0")
        
        frmSensorInfo.grid(row=position, column=0, sticky="nsew")

        lblSensorName.grid(row=0, column=0)
        lblSensorValue.grid(row=0, column=1)


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
        lblEditSensorX = ttk.Label(frmEditLocation, text="X: ")
        self.entEditSensorX = ttk.Entry(frmEditLocation)
        lblEditSensorX.grid(row=0, column=0, padx=5, pady=5,)
        self.entEditSensorX.grid(row=0, column=1, padx=5, pady=5)
        lblEditSensorY = ttk.Label(frmEditLocation, text="Y: ")
        self.entEditSensorY = ttk.Entry(frmEditLocation)
        lblEditSensorY.grid(row=1, column=0, padx=5, pady=5)
        self.entEditSensorY.grid(row=1, column=1, padx=5, pady=5)
        lblEditSensorZ = ttk.Label(frmEditLocation, text="Z: ")
        self.entEditSensorZ = ttk.Entry(frmEditLocation)
        lblEditSensorZ.grid(row=2, column=0, padx=5, pady=5)
        self.entEditSensorZ.grid(row=2, column=1, padx=5, pady=5)
        frmEditLocation.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        #save and discard buttons
        frmEditSensorSaveOrDiscard = ttk.Frame(self)
        btnEditSensorSave = ttk.Button(frmEditSensorSaveOrDiscard, text="Save and Exit", command=lambda: EditSensorPage.saveAndExit(self, controller))
        btnEditSensorSave.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        btnEditSensorDiscard = ttk.Button(frmEditSensorSaveOrDiscard, text="Discard and Exit", command=lambda: EditSensorPage.discardAndExit(self, controller))
        btnEditSensorDiscard.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        frmEditSensorSaveOrDiscard.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    
    def saveAndExit(self, controller):
        sensorX = self.entEditSensorX.get()
        sensorY = self.entEditSensorY.get()
        sensorZ = self.entEditSensorZ.get()

        self.entEditSensorX.delete(0, tk.END)
        self.entEditSensorY.delete(0, tk.END)
        self.entEditSensorZ.delete(0, tk.END)
        controller.show_frame(StartPage)

    def discardAndExit(self, controller):
        self.entEditSensorX.delete(0, tk.END)
        self.entEditSensorY.delete(0, tk.END)
        self.entEditSensorZ.delete(0, tk.END)
        controller.show_frame(StartPage)
