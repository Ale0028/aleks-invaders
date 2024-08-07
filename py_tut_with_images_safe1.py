# Import the pygame module
import pygame
import random
# Import random for random numbers

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH,SCREEN_HEIGHT = 800,600  

# Define some colour constants
BLACK,RED = (0, 0, 0), (255, 0, 0)
GREEN,BLUE = (0, 255, 0),(0, 0, 255)
GRAY = (200, 200, 200)
seconds,timer=0,0
# Define some other useful stuff
CollisionDone = 0
Lives = 5
# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    




# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        cloudlist=["cloud.png","th.jpg","cloud3.png"]
        cloudnum=random.randint(0,2)
        self.surf = pygame.image.load(cloudlist[cloudnum]).convert_alpha()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Define the explosion object extending pygame.sprite.Sprite
# Use an image for a better looking sprite

# Notice, we have overidden __new__ to enable us
# to pass some parameters when we create (instansiate) this class 
# In this case we pass the location of the player, so our explosion
# starts in the correct location.
class Explosion(pygame.sprite.Sprite):

    def __new__(cls, *args, **kwargs):
        
        return super().__new__(cls)

    def __init__(self, x, y):
        super(Explosion, self).__init__()
        self.surf = pygame.image.load("explosion.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                x,y
            )
        )

    # Move the explosion based on a constant speed
    # Remove it when it passes the left edge of the screen
    # and re-enable new collisions by setting CollisionDone to zero
    def update(self):
        self.rect.move_ip(-8, 0)
        if self.rect.right < 0:
            self.kill()
            global CollisionDone
            CollisionDone = 0



# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()
minute=0
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Create our 'player'
player = Player()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
explosions = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)


# Variable to keep our main loop running
running = True
program = True
# Our main loop - This code runs many times a second. This is the games frame rate.
# The screen is filled with our objects and text and is flipped at the end of this loop
# to give the illusion of motion. A series of still images presented quickly, one after the other
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Should we add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud, and add it to our sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)


    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of our enemies and clouds
    enemies.update()
    clouds.update()
    explosions.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Now draw any text we need, such as lives left, score etc. 

    # =================================================
    # To load a system font use SysFont
    # ================================================= 
    #font1 = pygame.font.SysFont('chalkduster.ttf', 72)

    font1 = pygame.font.Font('turok.ttf', 36)
    img = font1.render("Lives " + str(Lives), True, BLUE)

    # ==================================
    # To put a rectangle around the text
    # ==================================
    #rect = img.get_rect()
    #pygame.draw.rect(img, BLUE, rect, 1)

    screen.blit(img,(10,10)) 

    # We have hit an enemy, so lose a life


    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies) and (CollisionDone == 0):
    #if pygame.sprite.spritecollideany(player, enemies):
        Lives = Lives-1
        boomlist=["mixkit-epic-impact-afar-explosion-2782.wav","mixkit-fast-game-explosion-1688.wav"]
        boomnum=random.randint(0,1)
        boomlist[boomnum].play()
        # If so, remove the player
        # player.kill()
        collisioncounted=False
        # Prevent this code from running again until we set CollisionDone to 0
        CollisionDone = 1
        # Stop any moving sounds and play the collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()

        new_explosion = Explosion(player.rect.left, player.rect.top)
        explosions.add(new_explosion)
        all_sprites.add(new_explosion)

        # Stop the loop
        # running = False
    
    seconds=seconds+1
    if seconds==24:
        timer=timer+1
        seconds=0
    if timer==60:
        minute=minute+1
        timer=0
    img0 = font1.render( str(minute) + ":" + str("%02d" % timer), True, BLACK)
    screen.blit(img0,(500,0))
    # Flip everything to the display
    pygame.display.flip()

    # Ensure we maintain a constant frames per second rate.
    # You could increase this to make the game harder to play.
    # A conventional movie plays at around 24 fps.
    # If you miss this step out, your game will try and run as fast as your CPU will let it!
    
    clock.tick(24)
    if Lives==0:
        running=False


fract=(timer/60)*100

print(fract)        
screen.fill((100,200,200))
font2 = pygame.font.Font('Insigne display.otf', 100)
img2 = font2.render("You lose! " , True, BLACK)
screen.blit(img2,(275,50))
font2b = pygame.font.Font('turok.ttf', 59)
font2c = pygame.font.Font('turok.ttf', 53)
if minute==0:
    img3= font2b.render("You survived for " +str(timer)+ " seconds" ,True,BLACK)
else:
    img3= font2c.render("You survived for "+ str(minute)+"."+str(int(fract))+" minutes",True,BLACK)
    img4= font2c.render("or " + str(minute) + " minute(s) & "+ str(timer) + " seconds",True,BLACK)
    on=1

screen.blit(img3,(0,150))
if on ==1:
  screen.blit(img4,(10,200))  
pygame.display.flip()
pygame.time.delay(5000)
pygame.mixer.music.stop()
pygame.mixer.quit()
number = 1
print("%02d" % (number,))