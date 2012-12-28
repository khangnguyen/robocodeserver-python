import uuid 
import json

from twisted.internet import reactor, protocol
from twisted.protocols import basic

PORT = 9000


{
    "action": "create",
    "params": {
        "room_name": "Room 1", #unique
        }    
}

class Game(object):
    def __init__(self, name, creator):
        self.name = name
        self.state = "PENDING"
        self.creator = creator
        self.players = set()
        self.players.add(creator)

    def addPlayer(self, player):
        self.players.add(player)

class RobocodeServer(basic.LineReceiver):
    def __init__(self, games):
        self.games = games
        self.actionHandlers = {'enter': self.enterLobby,  
                               'create': self.createGame}

    def lineReceived(self, line):
        print line
        msg = json.loads(line)
        return self.actionHandlers[msg['action']](msg['params'])
    
    def enterLobby(self, params):
        # return 'pending' games
        return json.dumps({'status': 'success',
                           'content': [g.name for g in self.games if g.status == 'PENDING']})

    def createGame(self, params):
        #TODO: game's name uniqueness validation
        game = Game(params['room_name'], self)
        self.games[game.name] = game
        return json.dumps({'status': 'success'})

class RobocodeServerFactory(protocol.Factory):
    def __init__(self):
        self.games = {}
    def buildProtocol(self, addr):
        return RobocodeServer(self.games)

def onStart():
    print "Server ready!"

factory = RobocodeServerFactory()
reactor.listenTCP(PORT, factory)
reactor.callWhenRunning(onStart)
reactor.run()
