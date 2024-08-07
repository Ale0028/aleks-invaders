import pygame
import random

pygame.mixer.pre_init(44100,-16,2,512)
pygame.mixer.init()

foe1=pygame.image.load('LargeAlien.png')
foe1=pygame.transform.scale(foe1,(47,34))
foe2=pygame.image.load('alien2.png')
foe2=pygame.transform.scale(foe2,(47,34))
foe3=pygame.image.load('galaga.png')
foe3=pygame.transform.scale(foe3,(47,34))
saucer=pygame.image.load('UFO.png')
saucer=pygame.transform.scale(saucer,(100,34))

aliensprite=[foe1,foe2,foe3]

clock = pygame.time.Clock()
fps = 60
game_over=0
screen_width = 600
screen_height = 800
pygame.font.init()
shoot_sound=pygame.mixer.Sound('Falling_putter.ogg')
explo_sound=pygame.mixer.Sound('mixkit-fast-game-explosion-1688.wav')
explo_sound.set_volume(0.5)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Spacey')

fontA=pygame.font.SysFont('turok.ttf',30)
fontB=pygame.font.SysFont('turok.ttf',40)

rows,cols=5,5
alien_cooldown=990
last_alienshot=pygame.time.get_ticks()
countdown=3
last_count=pygame.time.get_ticks()


red=(255,0,0)
green=(0,255,0)
white=(255,255,255)

bg = pygame.image.load("backgrond.png")
bg = pygame.transform.scale(bg,(screen_width,screen_height))
def draw_bg():
	screen.blit(bg, (0, 0))

def draw_txt(text,font,text_col,x,y):
	img=font.render(text,True,text_col)
	screen.blit(img,(x,y))

class ship(pygame.sprite.Sprite):
	def __init__(self, x,y,health):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load('spaceship.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y] 
		self.health_start=health
		self.health_remain=health
		self.last_shot=pygame.time.get_ticks()

	def update(self):
		speed=8
		cooldown=500
		game_over=0
		key=pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left>=0:
			self.rect.x-=speed
		if key[pygame.K_RIGHT] and self.rect.right<screen_width:
			self.rect.x+=speed
		time_now = pygame.time.get_ticks()
		if key[pygame.K_SPACE] and time_now-self.last_shot>cooldown:
			bullet=bullets(self.rect.centerx,self.rect.top)
			bullet_group.add(bullet)
			self.last_shot = time_now
			shoot_sound.play()

		self.mask=pygame.mask.from_surface(self.image)

		#healthbar
		pygame.draw.rect(screen,red,(self.rect.x,(self.rect.bottom+10),self.rect.width,15))
		if self.health_remain>0:
			pygame.draw.rect(screen,green,(self.rect.x,(self.rect.bottom+10),int(self.rect.width*(self.health_remain/self.health_start)),15))
		elif self.health_remain<=0:
			explosi=explosion(self.rect.centerx,self.rect.centery,3)
			explosion_group.add(explosi)
			self.kill()
			game_over=-1
		return game_over
class bullets(pygame.sprite.Sprite):
	def __init__(self, x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("missile2.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y] 

	def update(self):
		self.rect.y -= 5
		if self.rect.bottom<0:
			self.kill()
		if pygame.sprite.spritecollide(self,alien_group,True):
			self.kill()
			explo_sound.play()
			explos= explosion(self.rect.centerx, self.rect.centery,3)
			explosion_group.add(explos)
class aliens(pygame.sprite.Sprite):
	def __init__(self, x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image= aliensprite[random.randint(0,2)] 
		self.rect = self.image.get_rect()
		self.rect.center=[x,y]
		self.direction=1
		self.movecount=0
	def update(self):
		self.rect.x+=self.direction
		self.movecount+=1
		if abs(self.movecount>75):
			self.direction*=-1
			self.movecount=-75

class alien_bullets(pygame.sprite.Sprite):
	def __init__(self, x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("alien_missle.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y] 

	def update(self):
		self.rect.y += 5
		if self.rect.top>screen_height:
			self.kill
		if pygame.sprite.spritecollide(self,spaceship_group,False,pygame.sprite.collide_mask):
			spaceship.health_remain-=1
			self.kill()
			explo_sound.play()
			explo= explosion(self.rect.centerx,self.rect.centery,1)
			explosion_group.add(explo)

class UFO(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self) 
		self.image=saucer
		self.rect=self.image.get_rect()
		self.rect.center=[x,y]
		self.flydirect=1
		self.moving=1
		self.ufo_wait=pygame.time.get_ticks()
		self.cool=5000

	def update(self):

		if len(alien_group)<=12 and self.ufo_wait<self.cool:
			self.rect.x+=3.5*self.flydirect
			if self.rect.left>(screen_width) or self.rect.right<0:
				
				self.flydirect*=-1
				print(self.ufo_wait)

		else:
			self.ufo_wait=pygame.time.get_ticks()
			self.cool+=100
			print(self.cool)


	

class explosion(pygame.sprite.Sprite):
	def __init__(self, x,y, size):
		pygame.sprite.Sprite.__init__(self)
		self.images=[]
		for num in range(1,11):
			img=pygame.image.load(f'Explod{num}.png')
			if size == 1:
				pygame.transform.scale(img, (20,20))
			if size == 2:
				pygame.transform.scale(img, (40,40))
			if size == 3:
				pygame.transform.scale(img, (160,160))
			self.images.append(img)
		self.index=0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter=0

	def update(self):
		explosionspeed=2 
		self.counter+=1
		if self.counter>=explosionspeed and self.index<len(self.images)-1:
			self.counter=0
			self.index+=1
			self.image=self.images[self.index]
		
		if self.index>= len(self.images)-1 and self.counter>= explosionspeed:
			self.kill()

spaceship_group=pygame.sprite.Group()
bullet_group=pygame.sprite.Group()
alien_group=pygame.sprite.Group()
alienbullet_group=pygame.sprite.Group()
explosion_group=pygame.sprite.Group()
Ufo_group=pygame.sprite.Group()
	

def create_aliens():
	for number in range(rows):
		for item in range(cols):
			alien=aliens(100+item*100,100+number*70)
			alien_group.add(alien)

create_aliens()

	
spaceship=ship(int(screen_width/2),screen_height-100,3)
spaceship_group.add(spaceship)
ufo=UFO(-48,40)
Ufo_group.add(ufo)


run = True
while run:
	clock.tick(fps)
	draw_bg()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	if countdown<=0:
		#random bullets
		time_now=pygame.time.get_ticks()
		if time_now - last_alienshot > alien_cooldown:
			attacker=random.choice(alien_group.sprites())
			alienbullet=alien_bullets(attacker.rect.centerx,attacker.rect.bottom)
			alienbullet_group.add(alienbullet)
			last_alienshot=time_now
		if len(alien_group)==0:
			game_over=1

		if game_over==0:
			game_over=spaceship.update()
			bullet_group.update()
			alien_group.update()
			alienbullet_group.update()
			Ufo_group.update()
		else:
			if game_over==-1:
				draw_txt('GAME OVER!',fontB,white,int(screen_width/2-100),int(screen_height/2+50))
			if game_over==1:
				draw_txt('YOU WIN',fontB,white,int(screen_width/2-100),int(screen_height/2+50))


	if countdown>=0:
		draw_txt('GET READY!',fontB,white,int(screen_width/2-100),int(screen_height/2+50))
		draw_txt(str(countdown),fontB,white,int(screen_width/2-10),int(screen_height/2+10))
		count_timer= pygame.time.get_ticks()
		if count_timer-last_count>=1000:
			countdown-=1
			last_count=count_timer
	explosion_group.update()	
	spaceship_group.draw(screen)
	bullet_group.draw(screen)
	alien_group.draw(screen)
	alienbullet_group.draw(screen)
	explosion_group.draw(screen)
	Ufo_group.draw(screen)


	pygame.display.update()
	
pygame.quit()