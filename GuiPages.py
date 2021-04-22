import tkinter as tk
from tkinter import ttk

#  future plans
# class GuiPage(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        btnCreateRoom = ttk.Button(self, text="Create room", command=lambda: controller.show_frame(EditRoomPage))
        btnCreateRoom.grid(row=0, column=0, padx=5, pady=5)

        

        roomTabs = ttk.Notebook(self)

        roomFrame = ttk.Frame(roomTabs)
        roomTabs.add(roomFrame, text="room 1")
        roomTabs.grid(row=1, column=0, sticky="nsew")

        #legend Frame
        frmLegend = ttk.Frame(roomFrame)
        lblLegend = ttk.Label(frmLegend, text="Legend")

        lblLegend.grid(row=0, column=0, padx=5, pady=5)

        frmLegend.grid(row=0, column=0, padx=5, pady=5)
        #Room info frame
        frmRoomInfo = ttk.Frame(roomFrame)
        lblRoomInfoName = ttk.Label(frmRoomInfo, text="room 1")

        lblRoomInfoName.grid(row=0, column=0, padx=5, pady=5)

        frmRoomInfo.grid(row=0, column=1, padx=5, pady=5)

        #Sensor add button
        frmSensorAdd = ttk.Frame(roomFrame)
        btnAddSensor = ttk.Button(frmSensorAdd, text="Add Sensor", command=lambda: controller.show_frame(EditSensorPage))
        btnAddSensor.pack(side=tk.LEFT)
        frmSensorAdd.grid(row=1, column=0, padx=5, pady=5)


        #sensor list
        frmSensorList = ttk.Frame(roomFrame)
        canvasSensorList = tk.Canvas(frmSensorList)
        scrollbarSensorList = ttk.Scrollbar(frmSensorList, orient="vertical", command=canvasSensorList.yview)
        scrollable_frame = ttk.Frame(canvasSensorList)
        canvasSensorList.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvasSensorList.configure(yscrollcommand=scrollbarSensorList.set)
        
        canvasSensorList.bind("<Configure>", lambda e: canvasSensorList.configure(scrollregion = canvasSensorList.bbox("all") ))

        for i in range(100):
            frmSensorInfo = ttk.Frame(scrollable_frame, width=50, height=10, relief=tk.GROOVE, borderwidth=5)

            lblSensorName = ttk.Label(frmSensorInfo, text=f"Sensor id: {i}")
            lblSensorValue = ttk.Label(frmSensorInfo, text="value: 0.0")
            
            frmSensorInfo.grid(row=i, column=0, sticky="nsew")

            lblSensorName.grid(row=0, column=0)
            lblSensorValue.grid(row=0, column=1)

        canvasSensorList.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbarSensorList.pack(side=tk.RIGHT, fill="y")

        frmSensorList.grid(row=2, column=0, padx=5, pady=5)


        #3d vieuw placeholder
        frm3Dview = ttk.Frame(roomFrame)
        lbl3DTemp = ttk.Label(frm3Dview, font=('Helvetica', 30), text="3d placeholder")
        lbl3DTemp.pack(fill=tk.BOTH)
        frm3Dview.grid(row=2, column=1, padx=5, pady=5)


        


class EditRoomPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Name
        frmEditRoomName = ttk.Frame(self)
        lblEditRoomName = ttk.Label(frmEditRoomName, text="Name: ")
        entEditRoomName = ttk.Entry(frmEditRoomName)
        lblEditRoomName.grid(row=0, column=0, padx=5, pady=5)
        entEditRoomName.grid(row=0, column=1, padx=5, pady=5)
        frmEditRoomName.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        #dimensions
        frmEditDimensions = ttk.Frame(self)
        lblEditRoomWidth = ttk.Label(frmEditDimensions, text="Width: ")
        entEditRoomWidth = ttk.Entry(frmEditDimensions)
        lblEditRoomWidth.grid(row=0, column=0, padx=5, pady=5,)
        entEditRoomWidth.grid(row=0, column=1, padx=5, pady=5)
        lblEditRoomLength = ttk.Label(frmEditDimensions, text="Length: ")
        entEditRoomLength = ttk.Entry(frmEditDimensions)
        lblEditRoomLength.grid(row=1, column=0, padx=5, pady=5)
        entEditRoomLength.grid(row=1, column=1, padx=5, pady=5)
        lblEditRoomHeight = ttk.Label(frmEditDimensions, text="Height: ")
        entEditRoomHeight = ttk.Entry(frmEditDimensions)
        lblEditRoomHeight.grid(row=2, column=0, padx=5, pady=5)
        entEditRoomHeight.grid(row=2, column=1, padx=5, pady=5)
        frmEditDimensions.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        #save and discard buttons
        frmEditSaveOrDiscard = ttk.Frame(self)
        btnEditRoomSave = ttk.Button(frmEditSaveOrDiscard, text="Save and Exit", command=lambda: controller.show_frame(StartPage))
        btnEditRoomSave.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        btnEditRoomDiscard = ttk.Button(frmEditSaveOrDiscard, text="Discard and Exit", command=lambda: controller.show_frame(StartPage))
        btnEditRoomDiscard.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        frmEditSaveOrDiscard.grid(row=2, column=0, padx=5, pady=5, sticky="w")
class EditSensorPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #dimensions
        frmEditLocation = ttk.Frame(self)
        lblEditSensorX = ttk.Label(frmEditLocation, text="X: ")
        entEditSensorX = ttk.Entry(frmEditLocation)
        lblEditSensorX.grid(row=0, column=0, padx=5, pady=5,)
        entEditSensorX.grid(row=0, column=1, padx=5, pady=5)
        lblEditSensorY = ttk.Label(frmEditLocation, text="Y: ")
        entEditSensorY = ttk.Entry(frmEditLocation)
        lblEditSensorY.grid(row=1, column=0, padx=5, pady=5)
        entEditSensorY.grid(row=1, column=1, padx=5, pady=5)
        lblEditSensorZ = ttk.Label(frmEditLocation, text="Z: ")
        entEditSensorZ = ttk.Entry(frmEditLocation)
        lblEditSensorZ.grid(row=2, column=0, padx=5, pady=5)
        entEditSensorZ.grid(row=2, column=1, padx=5, pady=5)
        frmEditLocation.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        #save and discard buttons
        frmEditSensorSaveOrDiscard = ttk.Frame(self)
        btnEditSensorSave = ttk.Button(frmEditSensorSaveOrDiscard, text="Save and Exit", command=lambda: controller.show_frame(StartPage))
        btnEditSensorSave.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        btnEditSensorDiscard = ttk.Button(frmEditSensorSaveOrDiscard, text="Discard and Exit", command=lambda: controller.show_frame(StartPage))
        btnEditSensorDiscard.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        frmEditSensorSaveOrDiscard.grid(row=2, column=0, padx=5, pady=5, sticky="w")
