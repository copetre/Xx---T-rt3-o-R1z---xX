import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, hud):
        super().__init__()
        # pygame
        self.hud = hud

        # attributes
        self.health = 3
        self.max_health = 3
        self.attack = 1
        self.velocity = 4
        self.death = False

        # player box
        self.currentSprite = pygame.transform.scale(pygame.image.load('asset/jake_def.png'), (160, 160))
        self.rect = self.currentSprite.get_rect()
        self.rect.x = 50
        self.rect.y = 380

        # Sound
        self.sound = pygame.mixer.Channel(0)

        # jump
        self.jumping = False
        self.floating = False
        self.jumpingVelocity = 0.5
        self.jumpFrame = 0

        # animation déplacement
        self.walkAnimationRight = False
        self.walkAnimationLeft = False
        self.spritesWalkRight = [pygame.transform.scale(pygame.image.load('asset/jake_def.png'), (160, 160)),
                                 pygame.transform.scale(pygame.image.load('asset/jake_walk.png'), (160, 160))]
        self.spritesWalkLeft = [pygame.transform.flip(self.spritesWalkRight[0], True, False),
                                pygame.transform.flip(self.spritesWalkRight[1], True, False)]
        self.walkFrame = 0

        # animation dommage/mort
        self.damaged = False
        self.damagedFrame = 0
        self.spriteDeath = pygame.transform.scale(pygame.image.load('asset/jake_death.png'), (160, 160))

    def right(self):
        if self.sound.get_busy() == False:
            self.sound.play(pygame.mixer.Sound('SoundMusic/MarcheJack.ogg'), 1)
        self.walkAnimationRight = True
        self.rect.x += self.velocity

    def left(self):
        if self.sound.get_busy() == False:
            self.sound.play(pygame.mixer.Sound('SoundMusic/MarcheJack.ogg'), 1)
        self.walkAnimationLeft = True
        self.rect.x -= self.velocity

    def jump(self):
        # only jumps if on ground
        if(self.rect.y == 380):
            self.jumping = True
            self.sound.play(pygame.mixer.Sound('SoundMusic/JackSaut.ogg'), 0)

    def gravity(self):
        # if we are jumping, continue going upwards
        if(self.jumping):
            # move upwards
            self.rect.y = self.rect.y - self.jumpingVelocity

            # increase y-velocity
            self.jumpingVelocity = self.jumpingVelocity + 0.5
            
            # if velocity too high, disable jump
            if(self.jumpingVelocity>12):
                self.jumping = False
                self.floating = True
                self.jumpingVelocity = 1
        # else if we are right after a jump, float for a couple frames
        elif(self.floating):
            self.jumpingVelocity += 1
            if(self.jumpingVelocity>4):
                self.floating = False
                self.jumpingVelocity = 0.5
        # else and if necessary, apply gravity
        elif(self.rect.y < 380):
            # move downwards (but cap at ground y-level=380)
            self.rect.y = min(self.rect.y + self.jumpingVelocity, 380)

            # increase y-velocity
            self.jumpingVelocity = self.jumpingVelocity + 0.5
        # reset jumping velocity if done
        else:
            self.jumpingVelocity = 1

    def damage(self):
        if(self.health>0):
            self.sound.play(pygame.mixer.Sound('SoundMusic/JackAttaqué.ogg'), 0)
            self.health -= 1
            self.hud.loseHeart()
            self.damaged = True
        if(self.health==0):
            self.death = True
            self.walkAnimationRight = False
            self.walkAnimationLeft = False
            self.currentSprite = self.spriteDeath
    
    # visual refresh of Jack with animations
    def refresh(self, screen):
        # if walking in any direction, increase frame
        if(self.walkAnimationLeft or self.walkAnimationRight):
            self.walkFrame = (self.walkFrame+1) % 12 # %12 because we have 2 frames * 6 ticks each
        
        # set current sprite
        if(self.walkAnimationLeft):
            self.currentSprite = self.spritesWalkLeft[self.walkFrame//6] # //6 because update every 6 ticks
        elif(self.walkAnimationRight):
            self.currentSprite = self.spritesWalkRight[self.walkFrame//6] # //6 because update every 6 ticks
        
        # if we've been damaged, increase damaged frame (same if we are dead)
        if(self.damaged or self.death):
            self.damagedFrame += 1
            if(self.damaged and self.damagedFrame==37): # stop animation
                self.damaged = False
                self.damagedFrame = 0

        # do the actual update (if we have been hit, skip 1 in 2 frames)
        if (self.damagedFrame%8 < 4):
            screen.blit(self.currentSprite, self.rect) 
