import pygame, sys

class Character(object):
    def control(self, key, event):
        if key == pygame.K_ESCAPE:
            sys.exit()
