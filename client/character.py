import pygame, sys

class Character(object):
    def control(self, key):
        if key == pygame.K_ESCAPE:
            sys.exit()
