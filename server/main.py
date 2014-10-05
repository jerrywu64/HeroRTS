import json, math

from twisted.internet import protocol, reactor, task, endpoints

from game_map import GameMap
from hero import Hero
from unit import Unit

# Global flags for main loop
running = False
done = False

# Global game map
game_map = None

class GameProtocol(protocol.Protocol):
    def connectionMade(self):
        print "Connection made!"
        global running
        running = True
        # FIXME: Assumes hero for now
        self.client_type = "hero"

    def connectionLost(self, reason):
        global running, done
        running = False
        done = True

    def dataReceived(self, data):
        json_data = json.loads(data)
        if json_data["message_type"] == "map_request":
            print "map_request recvd!"
            self.transport.write(json.dumps({
                "message_type": "hello",
                "map": game_map.map_inp,
                "rows": game_map.rows,
                "cols": game_map.cols,
                "people": [p.dictify() for p in game_map.people]
            }) + "\n")
        elif json_data["message_type"] == "update":
            print json_data
        else:
            print "Unknown message type"
        

class GameProtocolFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return GameProtocol()

def init():
    global game_map
    game_map = GameMap(20, 20, [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        ], [Hero(10, 11.0, 11.0, math.pi/2), Unit(10, 1.5, 1.5, 0)])

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
    init()
    endpoints.serverFromString(reactor, "tcp:9999").listen(GameProtocolFactory())
    tick = task.LoopingCall(main_loop)
    tick.start(0.03)
    reactor.run()
