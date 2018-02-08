### Pygaman Game
### A platform shooter in the style of Jump-and-Shoot-Man
### Ben Gamber

import pygame

class Pygaman(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moveSpeed = 3

class Pellet(object):
    pass

class Baddie(object):
    pass

class Platform(object):
    pass

class Screen(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        pygame.display.set_mode((width, height))

def main():
    pygame.init()

    screen = Screen(800, 600)
    clock = pygame.time.Clock()

    playing = True
    while playing:
        for event in pygame.event.get():


            if event.type == pygame.QUIT:
                playing = False
    
    pygame.quit()

if __name__ == '__main__':
    main()