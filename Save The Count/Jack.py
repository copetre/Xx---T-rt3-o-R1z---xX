import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.health = 3
        self.max_health = 3
        self.attack = 1
        self.velocity = 2
        self.currentSprite = pygame.transform.scale(pygame.image.load('asset/jake_def.png'), (160, 160))
        self.rect = self.currentSprite.get_rect()
        self.rect.x = 50
        self.rect.y = 380
        self.jump = 0
        self.jump_high = 0
        self.jump_low = 0
        self.number_jump = 0
        self.has_jumped = False

        # animation
        self.screen = screen
        self.walkAnimationRight = False
        self.walkAnimationLeft = False
        self.spritesWalkRight = [pygame.transform.scale(pygame.image.load('asset/jake_def.png'), (160, 160)),
                                 pygame.transform.scale(pygame.image.load('asset/jake_walk.png'), (160, 160))]
        self.spritesWalkLeft = [pygame.transform.flip(self.spritesWalkRight[0], True, False),
                                pygame.transform.flip(self.spritesWalkRight[1], True, False)]
        self.walkFrame = 0

    def right(self):
        self.walkAnimationRight = True
        self.rect.x += self.velocity

    def left(self):
        self.walkAnimationLeft = True
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
    # visual refresh of Jack with animations
    def refresh(self):
        # if walking in any direction, increase frame
        if(self.walkAnimationLeft or self.walkAnimationRight):
            self.walkFrame = (self.walkFrame+1) % 12 # %12 because we have 2 frames * 6 ticks each
        
        # set current sprite
        if(self.walkAnimationLeft):
            self.currentSprite = self.spritesWalkLeft[self.walkFrame//6] # //6 because update every 6 ticks
        elif(self.walkAnimationRight):
            self.currentSprite = self.spritesWalkRight[self.walkFrame//6] # //6 because update every 6 ticks
        
        # do the actual update
        self.screen.blit(self.currentSprite, self.rect) 
