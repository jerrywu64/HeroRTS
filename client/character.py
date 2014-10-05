import pygame, sys

class Character(object):
    def key_control(self, key, event):
        if key == pygame.K_ESCAPE:
            sys.exit()
