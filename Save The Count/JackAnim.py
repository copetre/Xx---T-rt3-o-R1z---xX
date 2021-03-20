import pygame, sys

class Player(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y):
		super().__init__()
		self.move = False
		self.spritesAtck = [pygame.image.load('JackAnim.py'),pygame.image.load('JackAnim.py')]
		self.spitesWalk = [pygame.image.load('JackAnim.py'),pygame.image.load('JackAnim.py')]
		self.current_sprite = 0
		self.image = self.sprites[self.current_sprite]
		self.current_sprite = 0
		self.attack_animation = False

	def attack(self):
		self.attack_animation = True

	def update(self,speed):
		if self.attack_animation == True:
			self.current_sprite += speed
			if int(self.current_sprite) >= len(self.sprites):
				self.current_sprite = 0
				self.attack_animation = False

		self.image = self.sprites[int(self.current_sprite)]

# General setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Sprite Animation")

# Creating the sprites and groups
x = 100
y = 100
moving_sprites = pygame.sprite.Group()
player = Player(x,y)
moving_sprites.add(player)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			moving_sprites.remove(player)
			x-=10
			player = Player(x,y)
			moving_sprites.add(player)
		if keys[pygame.K_RIGHT]:
			moving_sprites.remove(player)
			x+=10
			player = Player(x, y)
			moving_sprites.add(player)
		if keys[pygame.K_UP]:
			moving_sprites.remove(player)
			y-=10
			player = Player(x, y)
			moving_sprites.add(player)
		if keys[pygame.K_DOWN]:
			moving_sprites.remove(player)
			y+=10
			player = Player(x, y)
			moving_sprites.add(player)
		if keys[pygame.K_a]:
			player.attack()

	# Drawing
	screen.fill((0,0,0))
	moving_sprites.draw(screen)
	moving_sprites.update(0.25)
	pygame.display.flip()
	clock.tick(60)