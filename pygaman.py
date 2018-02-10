### Pygaman Game
### A platform shooter in the style of Jump-and-Shoot-Man
### Ben Gamber

import pygame

# Player's character - Jumps and shoots!
class Pygaman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Pygaman, self).__init__()
        self.x = x
        self.y = y
        self.move_speed = 0
        self.vert_speed = 0
        self.run1 = pygame.image.load('pygaman1.png').convert_alpha()
        self.run2 = pygame.image.load('pygaman2.png').convert_alpha()
        self.jump = pygame.image.load('pygaman3.png').convert_alpha()
        self.run_anim = [self.run1, self.run2]
        self.direction = 'right'
        self.rect = pygame.Rect(self.x, self.y, 30, 40)
        self.jump_count = 0
        self.stage_complete = False

    def update(self, window, platforms):
        self.rect = pygame.Rect(self.x, self.y, 30, 40)
        self.gravity(window)

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if platform.is_goal == True:
                    self.stage_complete = True
                if self.rect.bottom >= (platform.rect.top + self.vert_speed) and \
                self.rect.right >= platform.rect.left and self.rect.left <= platform.rect.right and \
                self.vert_speed >= 0:
                    self.y = (platform.rect.top - self.rect.height) + 1
                    self.vert_speed = 0
                    self.jump_count = 0
        
        self.x += self.move_speed
        self.y += self.vert_speed

    # Handles sprite image selection based on movement
    def render(self, frames=20, counter=0):
        frame = counter % frames
        sprite_index = frame / (frames / 2)
        if self.vert_speed != 0:
            if self.direction == 'right':
                return self.jump
            elif self.direction == 'left':
                return pygame.transform.flip(self.jump, True, False)
        elif self.move_speed > 0:
            return self.run_anim[sprite_index]
        elif self.move_speed < 0:
            return pygame.transform.flip(self.run_anim[sprite_index], True, False)
        else:
            if self.direction == 'right':
                return self.run_anim[0]
            elif self.direction == 'left':
                return pygame.transform.flip(self.run_anim[0], True, False)

    # Handles player falling and stopping at edge of screen.
    def gravity(self, window):
        if (self.y + self.rect.height) >= (window.height - self.vert_speed) and self.vert_speed > 0:
            self.vert_speed = 0
            self.jump_count = 0
        elif (self.y + self.rect.height) < window.height:
            self.vert_speed += 0.5
            
    def shoot(self, pellets):
        if len(pellets) < 4:
            pellets.add(Pellet(self.x, self.y + 10, self.direction, speedmod=self.move_speed))

# Enemies! Get past them all to win!
class Baddie(pygame.sprite.Sprite):
    def __init__(self, x, y, move_speed=4, direction='right', moving=False):
        super(Baddie, self).__init__()
        self.x = x
        self.y = y
        self.img1 = pygame.image.load('baddie1.png').convert_alpha()
        self.img2 = pygame.image.load('baddie2.png').convert_alpha()
        self.walk_anim = [self.img1, self.img2]
        self.move_speed = move_speed
        self.vert_speed = 0
        self.direction = direction
        self.moving = moving
        self.shoot_counter = 0

    def update(self, window, platforms):
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.gravity(window)
        self.shoot_counter += 1

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.rect.bottom >= (platform.rect.top + self.vert_speed) and \
                self.rect.right >= platform.rect.left and self.rect.left <= platform.rect.right and \
                self.vert_speed >= 0:
                    self.y = (platform.rect.top - self.rect.height) + 1
                    self.vert_speed = 0

                if self.rect.left <= platform.rect.left:
                    self.direction = 'right'
                elif self.rect.right >= platform.rect.right:
                    self.direction = 'left'

        if self.direction == 'right' and self.move_speed < 0:
            self.move_speed = -self.move_speed
        elif self.direction == 'left' and self.move_speed > 0:
            self.move_speed = -self.move_speed
        
        if self.moving == True:
            self.x += self.move_speed
        
        self.y += self.vert_speed

    def render(self, frames=10, counter=0):
        if self.moving == True:
            frame = counter % frames
            sprite_index = frame / (frames / 2)
            return self.walk_anim[sprite_index]
        else:
            return self.walk_anim[0]

    def gravity(self, window):
        if (self.y + self.rect.height) >= (window.height - self.vert_speed) and self.vert_speed > 0:
            self.vert_speed = 0
            self.jump_count = 0
        elif (self.y + self.rect.height) < window.height:
            self.vert_speed += 0.5

    def shoot(self, badpellets):
        badpellets.add(BadPellet(self.x, self.y + 10, self.direction))

# Bullets fired by the player!
class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speedmod=0):
        super(Pellet, self).__init__()
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 5
        self.speedmod = speedmod
        self.img1 = pygame.image.load('pellet1.png').convert_alpha()
        self.img2 = pygame.image.load('pellet2.png').convert_alpha()
        self.sprites = [self.img1, self.img2]
        self.rect = self.img1.get_rect()
        self.target = type(Baddie)

    def update(self, window, baddies):
        self.rect = pygame.Rect(self.x, self.y, self.rect.height, self.rect.width)
        if self.direction == 'left' and self.speed > 0:
            self.speed = -self.speed
        self.x += self.speed + self.speedmod
        if self.x > window.width or self.x < 0:
            self.kill()
        self.detect_collision(baddies)

    def detect_collision(self, targets):
        for target in targets:
            if self.rect.colliderect(target.rect):
                target.kill()
                self.kill()

    def render(self, frames=20, counter=0):
        frame = counter % frames
        sprite_index = frame / (frames / len(self.sprites))
        return self.sprites[sprite_index]

class BadPellet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super(BadPellet, self).__init__()
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 6
        self.img1 = pygame.image.load('badpellet1.png').convert_alpha()
        self.img2 = pygame.image.load('badpellet2.png').convert_alpha()
        self.sprites = [self.img1, self.img2]
        self.rect = self.img1.get_rect()
        self.target = type(Pygaman)

    def update(self, window, player):
        self.rect = pygame.Rect(self.x, self.y, self.rect.height, self.rect.width)
        if self.direction == 'left' and self.speed > 0:
            self.speed = -self.speed
        self.x += self.speed
        if self.x > window.width or self.x < 0:
            self.kill()
        self.detect_collision(player)
    
    def detect_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.kill()
            self.kill()

    def render(self, frames=20, counter=0):
        frame = counter % frames
        sprite_index = frame / (frames / len(self.sprites))
        return self.sprites[sprite_index]

# Platforms for the player to jump on!
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(255, 255, 255), is_goal=False):
        super(Platform, self).__init__()
        self.x = x
        self.y = y
        self. width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.is_goal = is_goal

    def getRect(self):
        return (self.x, self.y, self.width, self.height)

# Handles screen size
class Window(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

def main():
    bg = (10, 25, 50)
    white = (255, 255, 255)
    red = (250, 10, 10)
    blue = (25, 50, 250)
    pygame.init()
    window = Window(800, 600)
    clock = pygame.time.Clock()
    textF = pygame.font.Font(pygame.font.get_default_font(), 36)
    textB = pygame.font.Font(pygame.font.get_default_font(), 38)
    players = pygame.sprite.Group()
    player = Pygaman(40, 550)
    players.add(player)
    pellets = pygame.sprite.Group()

    baddies = pygame.sprite.Group()
    badpellets = pygame.sprite.Group()

    platforms = pygame.sprite.Group()

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
        Platform(300, 545, 50, 10),
        Platform(400, 550, 200, 10),
        Platform(30, 75, 20, 20, color=blue, is_goal=True)
    ]

    enemies0 = [

    ]

    enemies1 = [
        Baddie(145, 140, moving=True),
        Baddie(200, 550, direction='left', moving=False)
    ]

    stages = [stage0, stage1]
    enemies = [enemies0, enemies1]
    current_stage = 1 ## Reset to 0 for game start
    counter = 0
    death_timer = 0
    win_timer = 0
    playing = True
    while playing:
        if counter == 0:
            for platform in platforms:
                platform.kill()
            for platform in stages[current_stage]:
                platforms.add(platform)
            for enemy in enemies[current_stage]:
                baddies.add(enemy)
        counter += 1
        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_RIGHT]:
                player.direction = 'right'
                player.move_speed = 3
            elif pressed[pygame.K_LEFT]:
                player.direction = 'left'
                player.move_speed = -3
            else:
                player.move_speed = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and player.jump_count < 2:
                player.vert_speed = -7
                player.jump_count += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot(pellets)
            if event.type == pygame.QUIT:
                playing = False

        window.screen.fill(bg)
        for player in players:
            player.update(window, platforms)
            window.screen.blit(player.render(counter=counter), (player.x, player.y))
        for baddie in baddies:
            baddie.update(window, platforms)
            if counter % 120 == 0:
                baddie.shoot(badpellets)
            window.screen.blit(baddie.render(counter=counter), (baddie.x, baddie.y))
        for pellet in pellets:
            pellet.update(window, baddies)
            window.screen.blit(pellet.render(counter=counter), (pellet.x, pellet.y))
        for badpellet in badpellets:
            badpellet.update(window, player)
            window.screen.blit(badpellet.render(counter=counter), (badpellet.x, badpellet.y))
        for platform in stages[current_stage]:
            pygame.draw.rect(window.screen, platform.color, platform.getRect(), 0)

        if player.stage_complete == True:
            window.screen.blit(textB.render('YOU WIN', 0, bg), (299, 249))
            window.screen.blit(textF.render('YOU WIN', 0, blue), (300, 250))
            win_timer += 1
            if win_timer >= 100:
                playing = False ## TODO: Load new stage here
        elif len(players) < 1:
            window.screen.blit(textB.render('YOU LOSE', 0, bg), (299, 249))
            window.screen.blit(textF.render('YOU LOSE', 0, red), (300, 250))
            death_timer += 1
            if death_timer >= 100:
                playing = False

        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()

if __name__ == '__main__':
    main()