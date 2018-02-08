### Pygaman Game
### A platform shooter in the style of Jump-and-Shoot-Man
### Ben Gamber

import pygame

class Pygaman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Pygaman, self).__init__()
        self.x = x
        self.y = y
        self.moveSpeed = 0
        self.vertSpeed = 0
        self.img1 = pygame.image.load('pygaman1.png').convert_alpha()
        self.img2 = pygame.image.load('pygaman2.png').convert_alpha()
        self.sprites = [self.img1, self.img2]
        self.direction = 'right'
        self.rect = self.img1.get_rect()
        self.jumpCount = 0

    def update(self, window):
        self.x += self.moveSpeed

        self.gravity(window)
        self.y += self.vertSpeed

    def render(self, frames=20, counter=0):
        frame = counter % frames
        sprite_index = frame / (frames / 2)
        if self.moveSpeed > 0:
            return self.sprites[sprite_index]
        elif self.moveSpeed < 0:
            return pygame.transform.flip(self.sprites[sprite_index], True, False)
        else:
            if self.direction == 'right':
                return self.sprites[0]
            elif self.direction == 'left':
                return pygame.transform.flip(self.sprites[0], True, False)

    def gravity(self, window):
        if (self.y + self.rect.height) >= (window.height - self.vertSpeed) and self.vertSpeed > 0:
            self.vertSpeed = 0
            self.jumpCount = 0
        elif (self.y + self.rect.height) < window.height:
            self.vertSpeed += 0.5

class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speedmod=0):
        super(Pellet, self).__init__()
        self.x = x
        self.y = y
        self.speed = 5
        self.speedmod = speedmod
        self.img1 = pygame.image.load('pellet1.png').convert_alpha()
        self.img2 = pygame.image.load('pellet2.png').convert_alpha()
        self.sprites = [self.img1, self.img2]
        self.direction = direction
        self.rect = self.img1.get_rect()

    def update(self, window):
        if self.direction == 'left':
            self.speed = -self.speed
            self.direction = 'leftx'
        self.x += self.speed + self.speedmod
        if self.x > window.width or self.x < 0:
            self.kill()

    def render(self, frames=20, counter=0):
        frame = counter % frames
        sprite_index = frame / (frames / len(self.sprites))
        return self.sprites[sprite_index]

class Baddie(object):
    pass

class Platform(object):
    pass

class Window(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

def main():
    bg = (10, 25, 50)
    pygame.init()
    window = Window(800, 600)
    clock = pygame.time.Clock()

    player = Pygaman(40, 40)

    pellets = pygame.sprite.Group()

    counter = 0
    playing = True
    while playing:
        counter += 1
        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RIGHT]:
                player.direction = 'right'
                player.moveSpeed = 3
            elif pressed[pygame.K_LEFT]:
                player.direction = 'left'
                player.moveSpeed = -3
            else:
                player.moveSpeed = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and player.jumpCount < 2:
                player.vertSpeed = -7
                player.jumpCount += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pellets.add(Pellet(player.x, player.y + 10, player.direction, speedmod=player.moveSpeed))
            if event.type == pygame.QUIT:
                playing = False

        window.screen.fill(bg)
        player.update(window)
        window.screen.blit(player.render(counter=counter), (player.x, player.y))
        for pellet in pellets:
            pellet.update(window)
            window.screen.blit(pellet.render(counter=counter), (pellet.x, pellet.y))
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()

if __name__ == '__main__':
    main()