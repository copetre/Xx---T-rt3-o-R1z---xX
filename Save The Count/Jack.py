import pygame
import math


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
        self.jump = 0
        self.jump_high = 0
        self.jump_low = 0
        self.number_jump = 0
        self.has_jumped = False

    def right(self):
        self.rect.x += self.velocity

    def left(self):
        self.rect.x -= self.velocity

    def jumping(self):
        if self.has_jumped:
            if self.jump_high >= 1.5:
                while self.rect.y < 390:

                    self.jump_low += 0.00001
                    self.jump = self.jump_low
                    self.rect.y += 9.81 * (self.jump / 2)
                    print("descend")
            else:
                self.jump_high += 0.01
                if self.jump_high < 0.1:
                    self.jump = self.jump_high
                    self.rect.y -= 9.81 * (self.jump / 2)
                    print("monte début")
                else :
                    self.jump = 0.1
                    self.rect.y -= 9.81 * (self.jump / 2)
                    print("monte fin")

        if self.jump_low > 0 and self.rect.y >= 390:
            self.jump_high = 0
            self.jump_low = 0
            self.has_jumped = False
            print("sol")
