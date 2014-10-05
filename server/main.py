import json

from twisted.internet import protocol, reactor, task, endpoints
# from twisted.protocols.basic import LineReceiver

# Global flags for main loop
running = False
done = False

class GameProtocol(protocol.Protocol):
    def connectionMade(self):
        print "Connection made!"
        global running
        running = True
        # FIXME: Assumes hero for now
        self.client_type = "hero"
        self.transport.write("HELLO\n")

    def connectionLost(self, reason):
        global running, done
        running = False
        done = True

    def dataReceived(self, data):
        hero_state = json.loads(data)
        # print hero_state

class GameProtocolFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return GameProtocol()

def main_loop():
    # Handle stopped, and done
    if done:
        global tick
        tick.stop()
        print "Done"
        return
    if not running: return
    # TODO: Do the main thing here
    # print "Running"

if __name__ == "__main__":
    endpoints.serverFromString(reactor, "tcp:9999").listen(GameProtocolFactory())
    tick = task.LoopingCall(main_loop)
    tick.start(0.03)
    reactor.run()
