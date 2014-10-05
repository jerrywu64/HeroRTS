import pygame
from twisted.internet import reactor

class Character(object):
    def key_control(self, key, event):
        if key == pygame.K_ESCAPE:
            reactor.stop()

    def mouse_control(self, mouse_pos):
        pass

    def click_control(self, mouse_pos, button):
        pass
