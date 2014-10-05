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
game_map = None
prot = None
recvd_hello = False

class GameClientProtocol(protocol.Protocol):
    def dataRecieved(self, data):
        print "dataReceived", data
        json_data = json.loads(data)
        if json_data["message_type"] == "hello":
            global recvd_hello
            recvd_hello = True
            people = []
            for p in json_data["people"]:
                if p["type"] == "hero":
                    people.append(Hero.from_dict(p))
                elif p["type"] == "unit":
                    people.append(Unit.from_dict(p))
                else:
                    raise Exception("Unknown person type")
            global game_map
            game_map = GameMap(json_data["rows"], json_data["cols"],
                               json_data["map"], people)
        elif json_data["message_type"] == "update":
            # TODO
            pass

    def sendMessage(self, msg):
        print "sendMessage"
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
    if game_map is not None:
        character.update(game_map)
        character.draw(game_map)
    else:
        # Loading...
        pass

    # Swap buffers to push display
    pygame.display.flip()

    # Send data
    if prot is not None:
        if game_map is None:
            if not recvd_hello:
                global recvd_hello
                recvd_hello = True
                prot.sendMessage(json.dumps({
                    "message_type": "map_request"}))
        else:
            prot.sendMessage(json.dumps({
                "message_type": "update",
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

    reactor.connectTCP("localhost", 9999, GameClientProtocolFactory())
    tick = task.LoopingCall(main_loop)
    tick.start(0.03)
    reactor.run()
