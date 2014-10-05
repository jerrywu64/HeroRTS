import json, math

from twisted.internet import protocol, reactor, task, endpoints

from game_map import GameMap
from commander import Commander
from hero import Hero
from unit import Unit
from util import incline
from bullet import Bullet
from random import random

# Global flags for main loop
done = False
hero_connected = False
commander_connected = False

# Global game map
game_map = None
hero = None
commander = None

class GameProtocol(protocol.Protocol):
    def connectionMade(self):
        print "Connection made!"
        self.client_type = None

    def connectionLost(self, reason):
        global running, done
        running = False
        done = True

    def dataReceived(self, data):
        json_data = json.loads(data)
        if json_data["message_type"] == "map_request":
            self.client_type = json_data["mode"]
            if self.client_type == "hero":
                global hero_connected
                hero_connected = True
            else:
                global commander_connected
                commander_connected = True
            print "map_request recvd!"
            self.transport.write(json.dumps({
                "message_type": "hello",
                "running": commander_connected and hero_connected,
                "map": game_map.map_inp,
                "rows": game_map.rows,
                "cols": game_map.cols,
                "hero": game_map.hero.dictify(),
                "commander": game_map.commander.dictify(),
                "units": [u.dictify() for u in game_map.units],
                "bullets": [b.dictify() for b in game_map.bullets]
            }) + "\n")
        elif json_data["message_type"] == "update":
            if self.client_type is None:
                self.transport.loseConnection()
            elif self.client_type == "hero":
                hero.location = json_data["location"]
                hero.orientation = json_data["orientation"]
                if json_data["fired"]:
                    b = hero.make_bullet(game_map)
                    game_map.bullets.append(b)
            elif self.client_type == "commander":
                commander.waypoints = json_data["waypoints"]

            # Respond with everything
            self.transport.write(json.dumps({
                "message_type": "update",
                "running": commander_connected and hero_connected,
                "hero": game_map.hero.dictify(),
                "commander": game_map.commander.dictify(),
                "units": [u.dictify() for u in game_map.units],
                "bullets": [b.dictify() for b in game_map.bullets]
            }) + "\n")
        else:
            print "Unknown message type"
        

class GameProtocolFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return GameProtocol()

def init():
    global game_map
    global hero
    global commander
    hero = Hero(10, 11.0, 11.0, math.pi/2)
    commander = Commander()
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
        ], hero, commander, [Unit(10, 10.5, 7.5, 0)])

def main_loop():
    # Handle stopped, and done
    if done:
        global tick
        tick.stop()
        print "Done"
        return
    if not hero_connected or not commander_connected: return

    # Update state
    global game_map
    for u in game_map.units:
        u.ai(game_map)
    new_bullets = []
    for b in game_map.bullets:
        out = b.move(game_map)
        if out is not False:
            if out == -1:
                hero.hp -= b.damage
                print "Hero hit", hero.hp
                if hero.hp <= 0:
                    hero.dead = True
                    print "HERO DEAD! D:"
            else:
                game_map.units[out].hp -= b.damage
                print "Unit hit", out, game_map.units[out].hp
                if game_map.units[out].hp <= 0:
                    print "Unit dead!"
                    # Remove the unit
                    game_map.units[out], game_map.units[-1] = game_map.units[-1], game_map.units[out]
                    game_map.units = game_map.units[:-1]
        else:
            new_bullets.append(b)
    game_map.bullets = new_bullets

if __name__ == "__main__":
    init()
    endpoints.serverFromString(reactor, "tcp:9999").listen(GameProtocolFactory())
    tick = task.LoopingCall(main_loop)
    tick.start(0.03)
    reactor.run()
