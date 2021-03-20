import pygame
import random

from Bullet import Bullet

class Policier(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.health = 2
        self.max_health = 2
        self.attack = 1
        self.image = pygame.transform.scale(pygame.image.load('asset/police_def.png'), (160, 160))
        self.rect = self.image.get_rect()
        self.all_bullets = pygame.sprite.Group()
        self.rect.x = 800
        self.rect.y = 380
        self.velocity = 4
        self.newpos = random.randint(5, 924)
        self.newpos -= self.newpos % self.velocity

    def move(self):

        if self.newpos > self.rect.x:
            self.rect.x += self.velocity
        elif self.newpos < self.rect.x:
            self.rect.x -= self.velocity
        else :
            self.newpos = random.randint(5, 924)
            self.newpos -= self.newpos % self.velocity


    def fire(self):
        self.all_bullets.add(Bullet(self))

