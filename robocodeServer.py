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

{
    "action": "join",
    "params": {
        "room_name": "Room 1",
        }
}

{
    "action": "move",
    "params": {
        "room_name": "Room 1",
        "moves": {} #undefined
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
        if player == self.creator:
            return "Creator is a player by default"
        if player in self.players:
            return "Player is in the game already"

        self.players.add(player)
        self.state = "STARTED"

    def makeMove(self, player, moves):
        print "Sender", player
        for p in self.players:
            print "Receiver", p
            if p != player:
                print "sending"
                p.sendLine(json.dumps(moves))

class RobocodeServer(basic.LineReceiver):
    def __init__(self, games):
        self.games = games
        self.actionHandlers = {'enter': self.enterLobby,  
                               'create': self.createGame,
                               'join': self.joinGame,
                               'move': self.makeMove}

    def dataReceived(self, line):
        print line
        try:
            msg = json.loads(line)            
            response = self.actionHandlers[msg['action']](msg.get('params', {}))
            if response: self.sendLine(response)
        except Exception, e:
            pass

    def enterLobby(self, params):
        # return 'pending' games        
        return json.dumps({'status': 'success',
                           'content': [n for n, g in self.games.iteritems() if g.state == 'PENDING']})

    def createGame(self, params):
        #TODO: game's name uniqueness validation
        game = Game(params['room_name'], self)
        self.games[game.name] = game
        return json.dumps({'status': 'success'})

    def joinGame(self, params):
        #TODO: check game existence
        game = self.games[params['room_name']]
        result = game.addPlayer(self)
        if result:
            return json.dumps({'status': 'fail', 'errors': [result,]})
        return json.dumps({'status': 'success'})

    def makeMove(self, params):
        #TODO: check game existence
        #TODO: check where game is playable
        game = self.games[params['room_name']]
        game.makeMove(self, params['moves'])
        
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
