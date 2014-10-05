import json, math, pygame, sys
from twisted.internet import protocol, reactor, task, endpoints

# TODO: Unhack this...
sys.path.append("../server")
from game_map import GameMap
from commander import Commander
from hero import Hero
from unit import Unit
from client_commander import ClientCommander
from client_hero import ClientHero
from bullet import Bullet

# Global client settings
mode = None # "hero" or "commander", based on cmd line args
character = None
game_map = None
prot = None

class GameClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.sendMessage(json.dumps({
            "message_type": "map_request",
            "mode": mode
        }))
    
    def dataReceived(self, data):
        # print "dataReceived", data
        json_data = json.loads(data)
        if json_data["message_type"] == "hello":
            global game_map
            print "Hello message"
            units = [Unit.from_dict(u) for u in json_data["units"]]
            bullets = [Bullet.from_dict(b) for b in json_data["bullets"]]
            hero = Hero.from_dict(json_data["hero"])
            commander = Commander.from_dict(json_data["commander"])
            game_map = GameMap(json_data["rows"], json_data["cols"],
                               json_data["map"], hero, commander, units, bullets)
        elif json_data["message_type"] == "update":
            # Drop any removed units/bullets, then update values for remaining
            if len(game_map.units) > len(json_data["units"]):
                game_map.units = game_map.units[:len(json_data["units"])]
            for i in xrange(len(json_data["units"]) - len(game_map.units)):
                game_map.units.append(Unit(1, 1999, 1999, 0, 0))
            for u_old, u_new in zip(game_map.units, json_data["units"]):
                u_old.update_from_dict(u_new)
            if len(game_map.bullets) > len(json_data["bullets"]):
                game_map.bullets = game_map.bullets[:len(json_data["bullets"])]
            for i in xrange(len(json_data["bullets"]) - len(game_map.bullets)):
                game_map.bullets.append(Bullet(0, 999, 999, 0, 0))
            for b_old, b_new in zip(game_map.bullets, json_data["bullets"]):
                b_old.update_from_dict(b_new)
            game_map.hero.update_from_dict(json_data["hero"])
            game_map.commander.update_from_dict(json_data["commander"])

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                character.click_control(event.pos, event.button)
        character.mouse_control(pygame.mouse.get_pos())

    # Clear screen
    screen.fill((255, 255, 255))
    if game_map is not None:
        for u in game_map.units:
            u.move(0, game_map)
        new_bullets = []
        for b in game_map.bullets:
            # Damage resolution is not done locally
            out = b.move(game_map)
            if out is False:
                new_bullets.append(b)
        game_map.bullets = new_bullets
        if character is None:
            if mode == "hero":
                print "Hero client"
                character = ClientHero(screen, game_map.hero)
            else:
                character = ClientCommander(screen, game_map.commander)
        character.update(game_map)
        character.draw(game_map)
    else:
        # Loading...
        pass

    # Swap buffers to push display
    pygame.display.flip()

    # Send data
    if prot is not None and game_map is not None:
        if mode == "hero":
            prot.sendMessage(json.dumps({
                "message_type": "update",
                "location": character.server_hero.location,
                "orientation": character.server_hero.orientation,
                "fired": character.fired,
            }))
        else:
            prot.sendMessage(json.dumps({
                "message_type": "update",
                "waypoints": character.server_commander.waypoints
            }))
        if mode == "hero" and character.fired:
            character.fired = False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Need to specify commander or hero"
        sys.exit()
    if (sys.argv[1] != "hero" and
        sys.argv[1] != "commander"):
        print "Need to specify commander or hero"
        sys.exit()
    else:
        print "Entering %s mode" % sys.argv[1]
    mode = sys.argv[1]
        
    pygame.init()
    # screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((620,480))

    reactor.connectTCP("localhost", 9999, GameClientProtocolFactory())
    tick = task.LoopingCall(main_loop)
    tick.start(0.03)
    reactor.run()
