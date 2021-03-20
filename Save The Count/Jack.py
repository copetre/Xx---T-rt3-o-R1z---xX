import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.health = 3
        self.max_health = 3
        self.attack = 1
        self.velocity = 1
        self.image = pygame.image.load('asset/jake_def.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 390

    def right(self):
        self.rect.x += self.velocity

    def left(self):
        self.rect.x -= self.velocity
