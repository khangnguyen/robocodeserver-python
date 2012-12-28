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
        self.transport.write(json.dumps({'action': 'enter'}))

    def lineReceived(self, line):
        print "line recveived on server-client1.py",line

class MyClientFactory(protocol.ClientFactory):
    protocol = MyClient


        
factory = MyClientFactory()
reactor.connectTCP(HOST, PORT, factory)

reactor.run()
