import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, policier):
        super().__init__()
        self.velocity = 5
        self.health = 1
        self.max_health = 1
        self.image = pygame.transform.scale(pygame.image.load('asset/Bullet.png'), (20, 10))
        self.rect = self.image.get_rect()
        self.rect.x = policier.rect.x-25
        self.rect.y = 461
        self.velocity = 6

    def move(self):
        self.rect.x -= self.velocity

