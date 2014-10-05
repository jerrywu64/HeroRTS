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
server_hero = None
game_map = None
prot = None

class GameClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.sendMessage(json.dumps({
            "message_type": "map_request"}))
    
    def dataReceived(self, data):
        # print "dataReceived", data
        json_data = json.loads(data)
        if json_data["message_type"] == "hello":
            units = [Unit.from_dict(u) for u in json_data["units"]]
            global server_hero
            server_hero = Hero.from_dict(json_data["hero"])
            global game_map
            game_map = GameMap(json_data["rows"], json_data["cols"],
                               json_data["map"], server_hero, units)
        elif json_data["message_type"] == "update":
            for u_old, u_new in zip(game_map.units, json_data["units"]):
                u_old.update_from_dict(u_new)
            global server_hero
            server_hero.update_from_dict(json_data["hero"])

    def sendMessage(self, msg):
        # print "sendMessage"
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
    global character
    if character is not None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                character.key_control(event.key, event.type)
        character.mouse_control(pygame.mouse.get_pos())

    # Clear screen
    screen.fill((255, 255, 255))
    if game_map is not None:
        if character is None:
            character = ClientHero(screen, server_hero)
        character.update(game_map)
        character.draw(game_map)
    else:
        # Loading...
        pass

    # Swap buffers to push display
    pygame.display.flip()

    # Send data
    if prot is not None and game_map is not None:
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

    reactor.connectTCP("localhost", 9999, GameClientProtocolFactory())
    tick = task.LoopingCall(main_loop)
    tick.start(0.03)
    reactor.run()
