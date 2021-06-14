import socketio

class SocketClientHandler():
    #Initialize socketIO client
    sio = socketio.Client(logger=False, engineio_logger=False)

    def __init__(self):
        #Start connect, print info and send message 
        self.sio.connect('http://localhost:5001')
        self.sio.on('json', self.handle_json)
    #Default socketIO events
    #-------------------------------------------------------------------------#
    @sio.event
    def connect():
        print('Connected with SocketIO server')

    @sio.event
    def connect_error(data):
        print("Connection with SocketIO server failed!")

    @sio.event
    def disconnect():
        print('Disconnected from SocketO server')

    @sio.event
    def message(data):
        print('Message from SocketIO server: ' + data)

    @sio.event
    def json(data):
        print('Message from SocketIO server: ' + data)

    def handle_json(self, json):
        # return json
        print('received json: ' + str(json))

    #-------------------------------------------------------------------------#

    @sio.event
    def sendMessage(self, data):
        self.sio.emit('message', data)

    @sio.event
    def createRoom(self, sid, roomname):
        self.sio.emit('enterRoom', {'username': sid, 'room': roomname })

    @sio.event
    def deleteRoom(self, sid, roomname):
        self.sio.emit('leaveRoom', {'username': sid, 'room': roomname })

    @sio.event
    def getAllRooms(self):
        self.sio.emit('getAllRooms')

# socketconn = SocketClientHandler()
# print('my sid is', socketconn.sio.sid)

# socketconn.my_event('TestRoom')
# socketconn.EnterRoom('TestRoom')
# socketconn.createRoom(socketconn.sio.sid, 'test')
# socketconn.deleteRoom(socketconn.sio.sid, 'test')
# socketconn.EnterRoom(socketconn.sio.sid, 'test2')
# socketconn.sendMessage('teleurgesteld')