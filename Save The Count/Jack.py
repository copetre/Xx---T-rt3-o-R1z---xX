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

        # animation déplacement
        self.screen = screen
        self.walkAnimationRight = False
        self.walkAnimationLeft = False
        self.spritesWalkRight = [pygame.transform.scale(pygame.image.load('asset/jake_def.png'), (160, 160)),
                                 pygame.transform.scale(pygame.image.load('asset/jake_walk.png'), (160, 160))]
        self.spritesWalkLeft = [pygame.transform.flip(self.spritesWalkRight[0], True, False),
                                pygame.transform.flip(self.spritesWalkRight[1], True, False)]
        self.walkFrame = 0

        # animation jump
        self.jumping = False
        self.jumpingVelocity = 0.5
        self.jumpFrame = 0

    def right(self):
        self.walkAnimationRight = True
        self.rect.x += self.velocity

    def left(self):
        self.walkAnimationLeft = True
        self.rect.x -= self.velocity

    def jump(self):
        # only jumps if on ground
        if(self.rect.y == 380):
            self.jumping = True

    def gravity(self):
        # if we are jumping, continue going upwards
        if(self.jumping):
            # move upwards
            self.rect.y = self.rect.y - self.jumpingVelocity

            # increase y-velocity
            self.jumpingVelocity = self.jumpingVelocity + 0.5
            
            # if velocity too high, disable jump
            if(self.jumpingVelocity>10):
                self.jumping = False
                self.jumpingVelocity = 1
        # else and if necessary, apply gravity
        elif(self.rect.y < 380):
            # move downwards (but cap at ground y-level=380)
            self.rect.y = min(self.rect.y + self.jumpingVelocity, 380)

            # increase y-velocity
            self.jumpingVelocity = self.jumpingVelocity + 0.5
        # reset jumping velocity if done
        else:
            self.jumpingVelocity = 1
    
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
