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
        self.run1 = pygame.image.load('pygaman1.png').convert_alpha()
        self.run2 = pygame.image.load('pygaman2.png').convert_alpha()
        self.jump = pygame.image.load('pygaman3.png').convert_alpha()
        self.run_anim = [self.run1, self.run2]
        self.direction = 'right'
        self.rect = self.run1.get_rect()
        self.jumpCount = 0

    def update(self, window):
        self.x += self.moveSpeed

        self.gravity(window)
        self.y += self.vertSpeed

    def render(self, frames=20, counter=0):
        frame = counter % frames
        sprite_index = frame / (frames / 2)
        if self.vertSpeed != 0:
            if self.direction == 'right':
                return self.jump
            elif self.direction == 'left':
                return pygame.transform.flip(self.jump, True, False)
        elif self.moveSpeed > 0:
            return self.run_anim[sprite_index]
        elif self.moveSpeed < 0:
            return pygame.transform.flip(self.run_anim[sprite_index], True, False)
        else:
            if self.direction == 'right':
                return self.run_anim[0]
            elif self.direction == 'left':
                return pygame.transform.flip(self.run_anim[0], True, False)

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

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super(Platform, self).__init__()
        self.x = x
        self.y = y
        self. width = width
        self.height = height

    def getRect(self):
        return (self.x, self.y, self.width, self.height)

class Window(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

def main():
    bg = (10, 25, 50)
    white = (255, 255, 255)
    pygame.init()
    window = Window(800, 600)
    clock = pygame.time.Clock()

    player = Pygaman(40, 550)

    pellets = pygame.sprite.Group()

    stage0 = [
        Platform(400, 600, 50, 10)
    ]

    stage1 = [
        Platform(50, 95, 50, 10),
        Platform(150, 145, 500, 10),
        Platform(700, 195, 50, 10),
        Platform(600, 245, 50, 10),
        Platform(500, 295, 50, 10),
        Platform(250, 345, 100, 10),
        Platform(400, 345, 100, 10),
        Platform(100, 395, 100, 10),
        Platform(200, 445, 50, 10),
        Platform(250, 495, 50, 10),
        Platform(300, 545, 50, 10)
    ]

    stages = [stage0, stage1]
    current_stage = 1 ## Reset to 0 for game start
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
        for platform in stages[current_stage]:
            pygame.draw.rect(window.screen, white, platform.getRect(), 0)
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()

if __name__ == '__main__':
    main()