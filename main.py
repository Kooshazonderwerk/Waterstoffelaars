import PySimpleGUI as sg
from Room import Room
from Sensor import Sensor
from Program import Program


def createSensorLayout(sensor):
	if(not isinstance(sensor, Sensor)):
		return [[]]

	sensorFrameLayout = [[sg.Text('sensor id: ' + sensor.getId()), sg.Text('value: ' + str(sensor.getValue()))]]
	sensorLayout = [sg.Frame('',sensorFrameLayout)]
	return sensorLayout

'''Takes a room object and returns a layout for that room to be used in the gui'''
def createRoomLayout(room):
	if(not isinstance(room, Room)):
		return [[]]

	legendFrameLayout = [
		[sg.T('legend')],
		[]
	]
	roomInfoFrameLayout = [
		[sg.T('room id: ' + str(room.getId()))]
	]

	graphicsViewLayout = [
		[sg.T('3d placeholder', font='Helvetica 60')]
	]

	sensors = room.getSensors()

	sensorsLayout = []
	for sensor in sensors:
		sensorsLayout.append(createSensorLayout(sensor))

	roomLayout = [
		[sg.Frame('legend', legendFrameLayout), sg.Frame('room info', roomInfoFrameLayout)],
		[sg.Column(sensorsLayout, scrollable=True, size=(220, 200), vertical_scroll_only=True), sg.Frame('3dview', graphicsViewLayout)]
	]
	return roomLayout

def sendRoomData(values):
	program.createRoom(values['roomName'], values['roomWidth'],values['roomHeight'],values['roomLength'])

def changeWindow(window, layout, newLayout):
	window[f'-COL{layout}-'].update(visible=False)
	window[f'-COL{newLayout}-'].update(visible=True)
	return newLayout

def initWindow(program):
	program.addRoomsFromNetwork()

	rooms = program.getRooms()

	roomLayouts = [[]]

	for room in rooms:
		roomLayouts[0].append(sg.Tab('room '+str(room.getId()), createRoomLayout(room)))


	#Room options layout
	roomOptionsLayout = [
		[sg.B('Create Room', key='createNewRoom')]
	]
	#main layout
	mainLayout = [  
		[sg.Frame('', roomOptionsLayout)],
		[sg.TabGroup(roomLayouts)]
		]



	#Room edit page layout
	roomNameLayout = [
		[sg.InputText(key='roomName')]
	]

	roomDimensionsLayout = [
		[sg.T('Width:')],
		[sg.InputText(key='roomWidth')],
		[sg.T('Length:')],
		[sg.InputText(key='roomLength')],
		[sg.T('Height:')],
		[sg.InputText(key='roomHeight')]
	]

	roomEditButtonsLayout = [
		[sg.B('Save and Exit', key='roomSaveExit')],
		[sg.B('Discard and Exit', key='roomDiscard')]
	]

	roomEditLayout = [
		[sg.Frame('Name', roomNameLayout)],
		[sg.Frame('Dimensions', roomDimensionsLayout)],
		[sg.Frame('', roomEditButtonsLayout)]
	]

	roomEdit = [
		[sg.Frame('RoomInfo',roomEditLayout )]
	]

	# Create the Window
	layout = [[sg.Column(mainLayout, key='-COL1-', visible=True), sg.Column(roomEdit, visible=False, key='-COL2-')],
		]

	return layout

sg.theme('LightGreen1')   # Add a touch of color
# All the stuff inside your window.
program = Program('http://localhost:5000')

layout = initWindow(program)

window = sg.Window('Window Title', layout)

layout = 1  # The currently visible layout

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
		break
	if layout == 1: # checking if current window is on the main page.
		if event == 'createNewRoom':
			layout = changeWindow(window, layout, 2)
	if layout == 2: # checking if current window is on the edit page.
		if event == 'roomSaveExit':
			sendRoomData(values)
			layout = 1
			tempLayout = initWindow(program)
			window1 = sg.Window('Window Title', tempLayout)
			window.close()
			window = window1

		if event == 'roomDiscard':
			layout = changeWindow(window, layout, 1)

window.close()



	