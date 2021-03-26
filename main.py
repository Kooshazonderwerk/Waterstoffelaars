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
		[sg.T('room id: ' + room.getId())]
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



sg.theme('LightGreen1')   # Add a touch of color
# All the stuff inside your window.
program = Program('http://localhost:5000')

program.addRoomsFromNetwork()

rooms = program.getRooms()

roomLayouts = [[]]

for room in rooms:
	roomLayouts[0].append(sg.Tab('room '+str(room.getId()), createRoomLayout(room)))


layout = [  [sg.TabGroup(roomLayouts)]
		]



# Create the Window
window = sg.Window('Window Title', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break

window.close()

