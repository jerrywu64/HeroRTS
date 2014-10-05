import json, math, pygame, sys
from twisted.internet import protocol, reactor, task, endpoints

# TODO: Unhack this...
sys.path.append("../server")
from game_map import GameMap
from hero import Hero
from unit import Unit
from client_hero import ClientHero

# Global client settings
character = None
prot = None

class GameClientProtocol(protocol.Protocol):
    def dataRecieved(self, data):
        # print data
        pass

    def sendMessage(self, msg):
        self.transport.write(msg + "\n")

class GameClientProtocolFactory(protocol.Factory):
    def buildProtocol(self, addr):
        print "buildProtocol"
        global prot
        prot = GameClientProtocol()
        return prot

    def startedConnecting(self, connector):
        print "startedConnecting"
    def clientConnectionLost(self, connector, reason):
        print "connection lost"
    def clientConnectionFailed(self, connector, reason):
        print "connection failed"

def main_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            character.key_control(event.key, event.type)
    character.mouse_control(pygame.mouse.get_pos())

    # Clear screen
    screen.fill((255, 255, 255))
    character.update(game_map)
    character.draw(game_map)

    # Swap buffers to push display
    pygame.display.flip()

    # Send data
    if prot is not None:
        prot.sendMessage(json.dumps({
            "location": character.loc,
            "orientation": character.orientation,
            "fired": False
        }))

if __name__ == "__main__":
    pygame.init()
    # screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((620,480))
    server_hero = Hero(10, 11.0, 11.0, math.pi/2.0)
    character = ClientHero(screen, server_hero)
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
        ], [Unit(10, 1.5, 1.5, 0)])

    reactor.connectTCP("localhost", 9999, GameClientProtocolFactory())
    tick = task.LoopingCall(main_loop)
    tick.start(0.03)
    reactor.run()
