import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
white = (255, 255, 255)
yellow = (255, 255, 0)
dark_orange = (255,140,0)
black = (0, 0, 0)
screensize = (SCREEN_WIDTH, SCREEN_HEIGHT)
clock = pygame.time.Clock()
FPS = 5

class BackGround(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class StartScreen(pygame.sprite.Sprite):
    def __init__(self, start_image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(start_image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/bjorns_face.png").convert_alpha()
        self.rect = self.surf.get_rect()

    # Move player based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)

    # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Beer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("images/beer" + str(random.randint(1,6)) + ".png").convert_alpha()
        self.rect = self.surf.get_rect()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/cass.png").convert_alpha()
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Initialize pygame
pygame.init()
BackGround = BackGround('images/background1.jpg', [0, 0])
StartScreen = StartScreen('images/startscreen1.jpg', [0,0])


#music
pygame.mixer.music.load('music/QoTSA.wav')
pygame.mixer.music.play(-1)

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(white)


#splash screen
splashscreen = True
while splashscreen:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            splashscreen = False

    screen.fill(black)

    font = pygame.font.Font('fonts/slkscre.ttf', 20)
    text = font.render("happy birthday bjorn :)", True, white)
    screen.blit(text, (460, 300))
    pygame.display.flip()

    font = pygame.font.Font('fonts/slkscre.ttf', 20)
    text = font.render("37!!!!!", True, white)
    screen.blit(text, (460, 400))
    pygame.display.flip()

    font = pygame.font.Font('fonts/slkscre.ttf', 20)
    text = font.render("art by jeonghye, python by jack", True, white)
    screen.blit(text, (460, 500))
    pygame.display.flip()

# start screen
startscreen = True
# color changer
COLORCHANGE = pygame.USEREVENT + 1
pygame.time.set_timer(COLORCHANGE, 250)

# start screen loop
while startscreen:
    count = 0
    colors = [white, dark_orange, yellow]
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            startscreen = False
    count += 1
    if count % 2 == 0:
        sel_color = colors[0]
    if count % 3 == 0:
        sel_color = colors[1]
    else:
        sel_color = colors[2]

    screen.fill((0, 0, 0))
    screen.blit(StartScreen.image, StartScreen.rect)
    font = pygame.font.Font('fonts/slkscre.ttf', 40)
    text = font.render("get 4 beers 4 10k won! avoid the cass!", True, yellow)
    screen.blit(text, (150, 640))
    pygame.display.flip()

# game function
def main():
    # local variables
    score = 0
    running = True

    # enemy adder
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 250)

    # instantiate player and enemey class
    player = Player()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # randomly generate the 'collectible' beers
    beerlist = pygame.sprite.Group()
    numBeer = 4
    for i in range(numBeer):
        b = Beer()
        b.rect.x = random.randint(0, screensize[0] - 100)
        b.rect.y = random.randint(200, screensize[1] - 100)
        beerlist.add(b)
        all_sprites.add(b)

    # main loop
    while running:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    pygame.QUIT
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        # register collision and count collectible beer
        beer_collected = pygame.sprite.spritecollide(player, beerlist, True)
        for i in beer_collected:
                score += 1

        # get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        # update enemy position
        enemies.update()

        # fill the screen
        screen.fill((0, 0, 0))
        screen.blit(BackGround.image, BackGround.rect)
        font = pygame.font.Font("fonts/slkscre.ttf", 60)
        text = font.render("Beers to go: " + str(4 - score), True, white)
        screen.blit(text, [400, 40])


        # draw player and sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            player.kill()
            running = False

        if len(beerlist) == 0:
            running = False

        # update the display
        pygame.display.flip()

    # endscreen
    endscreen = True
    while endscreen:
        screen.fill((0, 0, 0))
        screen.blit(BackGround.image, BackGround.rect)

        # text: happy birthday
        font = pygame.font.Font('fonts/slkscre.ttf', 60)
        text = font.render("happy bday bjorn :)", True, white)
        screen.blit(text, (280, 100))

        font = pygame.font.Font('fonts/slkscre.ttf', 40)
        text = font.render("space to play again, enter to quit", True, dark_orange)
        screen.blit(text, (195, 500))

        # switch between 'u won' and 'u lost'
        if score != 4:
            font = pygame.font.Font('fonts/slkscre.ttf', 40)
            text = font.render("but u lost :(", True, white)
            screen.blit(text, (550, 250))
        else:
            font = pygame.font.Font('fonts/slkscre.ttf', 40)
            text = font.render("good job! now we can drink!", True, white)
            screen.blit(text, (320, 250))

        # reset or exit game
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return pygame.quit()
                if event.key == K_SPACE:
                    main()
        pygame.display.flip()
main()