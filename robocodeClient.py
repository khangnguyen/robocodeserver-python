import json

from twisted.internet import reactor, protocol
from twisted.protocols import basic

HOST = 'localhost'
PORT = 9000

class MyClient(basic.LineReceiver):
    def connectionLost(self, reason=None):
        print "Connection lost", reason

    def connectionMade(self):
        print "connected!"
        self.transport.write(json.dumps({
                    "action": "create",
                    "params": {
                        "room_name": "Room 1"}
                    }))
    def lineReceived(self, line):
        response = json.loads(line)
        if not response.get('content'):
            self.transport.write(json.dumps({'action': 'enter'}))
        else:
            print response

class MyClientFactory(protocol.ClientFactory):
    protocol = MyClient


        
factory = MyClientFactory()
reactor.connectTCP(HOST, PORT, factory)

reactor.run()
