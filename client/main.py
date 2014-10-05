import pygame, sys

from hero import Hero

# Global client settings
character = None

if __name__ == "__main__":
    pygame.init()
    #screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((620,480))
    character = Hero(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN: character.control(event.key)

        # Clear screen
        screen.fill((255, 255, 255))
        character.draw()

        # Swap buffers to push display
        pygame.display.flip()
