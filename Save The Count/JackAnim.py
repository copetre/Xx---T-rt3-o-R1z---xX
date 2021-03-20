import pygame, sys, os


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.move = False
        self.spritesAtck = [pygame.image.load('asset/JakeBig.png'), pygame.image.load('asset/JakeBig.png'),
                            pygame.image.load('asset/JakeBig.png')]
        self.spritesWalk = [pygame.image.load('asset/JakeBig.png'), pygame.image.load('asset/JakeBig.png')]
        self.current_sprite = 0
        self.imageWalk = self.spritesWalk[self.current_sprite]
        self.imageAtck = self.spritesAtck[self.current_sprite]
        self.attack_animation = False

    def attack(self):
        self.attack_animation = True

    def walk(self):
        self.walk_animation = True

    def update(self, speed):
        if self.attack_animation == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.spritesAtck):
                self.current_sprite = 0
                self.attack_animation = False

        if self.walk_animation == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.spritesWalk):
                self.current_sprite = 0
                self.walk_animation = False

        self.imageWalk = self.spritesWalk[int(self.current_sprite)]
        self.imageAtck = self.spritesAtck[int(self.current_sprite)]
