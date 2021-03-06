### Pygaman Game
### A platform shooter in the style of Jump-and-Shoot-Man
### Ben Gamber

import pygame, copy

# Player's character - Jumps and shoots!
class Pygaman(pygame.sprite.Sprite):
    def __init__(self, x, y, direction='right'):
        super(Pygaman, self).__init__()
        self.x = x
        self.y = y
        self.move_speed = 0
        self.vert_speed = 0
        self.shoot_sound = pygame.mixer.Sound('audio/Pew__008.wav')
        self.death_sound = pygame.mixer.Sound('audio/Ouch__002.wav')
        self.jump_sound = pygame.mixer.Sound('audio/Jump__004.wav')
        self.win_sound = pygame.mixer.Sound('audio/Teleport__003.wav')
        self.run1 = pygame.image.load('pygaman1.png').convert_alpha()
        self.run2 = pygame.image.load('pygaman2.png').convert_alpha()
        self.jump = pygame.image.load('pygaman3.png').convert_alpha()
        self.run_anim = [self.run1, self.run2]
        self.direction = direction
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
        
        if not self.stage_complete:
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

    # Handles player falling and dying at edge of screen.
    def gravity(self, window):
        if self.y >= window.height:
            self.death_sound.play()
            self.kill() # Player dies if touching the bottom of the window

        self.vert_speed += 0.5
            
    def shoot(self, pellets):
        if len(pellets) < 4:
            self.shoot_sound.play()
            pellets.add(Pellet(self.x, self.y + 10, self.direction, speedmod=self.move_speed))

# Enemies! Get past them all to win!
class Baddie(pygame.sprite.Sprite):
    def __init__(self, x, y, move_speed=4, direction='right', moving=False):
        super(Baddie, self).__init__()
        self.x = x
        self.y = y
        self.death_sound = pygame.mixer.Sound('audio/Explosion__004.wav')
        self.img1 = pygame.image.load('baddie1.png').convert_alpha()
        self.img2 = pygame.image.load('baddie2.png').convert_alpha()
        self.walk_anim = [self.img1, self.img2]
        self.move_speed = move_speed
        self.vert_speed = 0
        self.direction = direction
        self.moving = moving
        self.shoot_counter = 0

    def update(self, window, platforms, player):
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.gravity(window)
        self.shoot_counter += 1

        if self.rect.colliderect(player.rect):
            player.x = -20
            player.y = -20
            player.death_sound.play()
            player.kill()

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.rect.bottom >= (platform.rect.top + self.vert_speed) and \
                self.rect.right >= platform.rect.left and self.rect.left <= platform.rect.right and \
                self.vert_speed >= 0:
                    self.y = (platform.rect.top - self.rect.height) + 1
                    self.vert_speed = 0

                if self.moving == True and self.rect.left <= platform.rect.left:
                    self.direction = 'right'
                elif self.moving == True and self.rect.right >= platform.rect.right:
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
        if self.y >= window.height:
            self.death_sound.play()
            self.kill() # Baddie dies if touching the bottom of the window
        else:
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
                target.death_sound.play()
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
            player.x = -20
            player.y = -20
            player.rect.x = -20
            player.rect.y = -20
            player.death_sound.play()
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
        pygame.display.set_caption('Pygaman')

def main():
    bg = (10, 25, 50)
    white = (255, 255, 255)
    red = (250, 10, 10)
    blue = (25, 50, 250)
    pygame.init()
    pygame.mixer.init()
    window = Window(800, 600)
    clock = pygame.time.Clock()
    textF = pygame.font.Font(pygame.font.get_default_font(), 36)
    textB = pygame.font.Font(pygame.font.get_default_font(), 38)
    text_lives = pygame.font.Font(pygame.font.get_default_font(), 12)
    instructions = pygame.font.Font(pygame.font.get_default_font(), 16)
    players = pygame.sprite.Group()
    pellets = pygame.sprite.Group()

    baddies = pygame.sprite.Group()
    badpellets = pygame.sprite.Group()

    platforms = pygame.sprite.Group()

    player_list = [
    Pygaman(50, 350),
    Pygaman(550, 500, direction='left'),
    Pygaman(90, 90)
    ]

    stage0 = [
        Platform(40, 400, 300, 10),
        Platform(350, 350, 50, 10),
        Platform(410, 400, 300, 10),
        Platform(700, 380, 20, 20, color=blue, is_goal=True)
    ]

    stage1 = [
        Platform(50, 95, 50, 10),
        Platform(150, 145, 500, 10),
        Platform(700, 195, 50, 10),
        Platform(600, 245, 50, 10),
        Platform(500, 295, 50, 10),
        Platform(400, 345, 100, 10),
        Platform(250, 345, 100, 10),
        Platform(100, 395, 100, 10),
        Platform(200, 445, 50, 10),
        Platform(250, 495, 50, 10),
        Platform(300, 545, 50, 10),
        Platform(400, 550, 200, 10),
        Platform(30, 75, 20, 20, color=blue, is_goal=True)
    ]

    stage2 = [
        Platform(80, 100, 50, 10),
        Platform(70, 400, 270, 10),
        Platform(360, 450, 50, 10),
        Platform(430, 400, 270, 10),
        Platform(700, 350, 50, 10),
        Platform(730, 330, 20, 20, color=blue, is_goal=True)
    ]

    enemies0 = [
        Baddie(350, 300, direction='left', moving=False)
    ]

    enemies1 = [
        Baddie(255, 490),
        Baddie(180, 390, moving=True),
        Baddie(400, 330, moving=True),
        Baddie(605, 220, direction='left'),
        Baddie(145, 140, moving=True),
        Baddie(345, 140, moving=True),
        Baddie(545, 140, moving=True),
    ]

    enemies2 = [
        Baddie(70, 360, moving=True),
        Baddie(110, 360, moving=True),
        Baddie(150, 360, moving=True),
        Baddie(430, 360, moving=True),
        Baddie(470, 360, moving=True),
        Baddie(510, 360, moving=True)
    ]

    music_list = [
        'audio/Juhani Junkala [Retro Game Music Pack] Level 1.wav',
        'audio/Juhani Junkala [Retro Game Music Pack] Level 2.wav',
        'audio/Juhani Junkala [Retro Game Music Pack] Level 3.wav',
    ]

    stages = [stage0, stage1, stage2]
    enemies = [enemies0, enemies1, enemies2]
    current_stage = 0
    counter = 0
    death_timer = 0
    win_timer = 0
    player_lives = 2
    playing = True
    while playing:
        if counter == 0:
            pygame.mixer.music.load(music_list[current_stage])
            pygame.mixer.music.set_volume(0.40)
            pygame.mixer.music.play(-1)
            death_timer = 0
            win_timer = 0
            if len(players) > 0:
                for player in players:
                    player.kill()
            player = copy.copy(player_list[current_stage])
            players.add(player)
            for platform in platforms:
                platform.kill()
            for platform in stages[current_stage]:
                platforms.add(platform)
            for baddie in baddies:
                baddie.kill()
            for enemy in enemies[current_stage]:
                baddies.add(copy.copy(enemy))
            for pellet in pellets:
                pellet.kill()
            for badpellet in badpellets:
                badpellet.kill()
        counter += 1

        if win_timer == 1:
            player_lives += 1
            pygame.mixer.music.stop()
            player.win_sound.play()
            if current_stage == len(stages) - 1:
                pygame.mixer.music.load('audio/Juhani Junkala [Retro Game Music Pack] Title Screen.wav')
                pygame.mixer.music.play(0)
        if death_timer == 1:
            pygame.mixer.music.stop()
            if player_lives == 0:
                pygame.mixer.music.load('audio/Juhani Junkala [Retro Game Music Pack] Ending.wav')
                pygame.mixer.music.play(0)

        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_RIGHT] and not player.stage_complete:
                player.direction = 'right'
                player.move_speed = 3
            elif pressed[pygame.K_LEFT] and not player.stage_complete:
                player.direction = 'left'
                player.move_speed = -3
            else:
                player.move_speed = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and \
            player.jump_count < 2 and not player.stage_complete:
                player.jump_sound.play()
                player.vert_speed = -7
                player.jump_count += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and \
            not player.stage_complete and len(players) > 0:
                player.shoot(pellets)
            if event.type == pygame.QUIT:
                playing = False

        window.screen.fill(bg)
        for player in players:
            player.update(window, platforms)
            window.screen.blit(player.render(counter=counter), (player.x, player.y))
        for baddie in baddies:
            baddie.update(window, platforms, player)
            if counter % 60 == 0:
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

        # Display Gameplay Instructions at start of game
        if current_stage == 0 and counter < 180:
            window.screen.blit(instructions.render('Left/Right Arrow: Move', 0, white), (100, 200))
            window.screen.blit(instructions.render('Up Arrow: Jump/Double Jump', 0, white), (100, 220))
            window.screen.blit(instructions.render('Spacebar: Shoot', 0, white), (100, 240))

        if player.stage_complete == True:
            if current_stage == len(stages) - 1: # Final Stage
                window.screen.blit(textB.render('YOU WIN', 0, bg), (299, 249))
                window.screen.blit(textF.render('YOU WIN', 0, blue), (300, 250))
                win_timer += 1
                if win_timer >= 180:
                    playing = False
            else:
                window.screen.blit(textB.render('STAGE COMPLETE', 0, bg), (249, 249))
                window.screen.blit(textF.render('STAGE COMPLETE', 0, blue), (250, 250))
                win_timer += 1
                if win_timer >= 90:
                    counter = 0
                    current_stage += 1

        elif len(players) < 1:
            if player_lives == 0:
                window.screen.blit(textB.render('YOU LOSE', 0, bg), (299, 249))
                window.screen.blit(textF.render('YOU LOSE', 0, red), (300, 250))
                death_timer += 1
                if death_timer >= 180:
                    pygame.mixer.music.stop()
                    playing = False
            else:
                window.screen.blit(textB.render('YOU DIED', 0, bg), (299, 249))
                window.screen.blit(textF.render('YOU DIED', 0, white), (300, 250))
                death_timer += 1
                if death_timer >= 90:
                    counter = 0
                    player_lives -= 1
        
        window.screen.blit(text_lives.render('Lives: %s' % player_lives, 0, white), (50, 550))

        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()

if __name__ == '__main__':
    main()