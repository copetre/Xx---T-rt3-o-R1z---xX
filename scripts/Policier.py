import pygame
import random

from .Bullet import Bullet

class Policier(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        # pygame
        self.game = game

        # attributes
        self.health = 2
        self.max_health = 2
        self.velocity = 4
        self.dead = False

        # policier box
        self.currentSprite = pygame.transform.scale(pygame.image.load('assets/police_def.png'), (160, 160))
        self.rect = self.currentSprite.get_rect()
        self.rect.x = 80 * random.randint(3, 10)
        self.rect.y = 380
        self.sound = pygame.mixer.Channel(2)
        self.facingRight = False

        # bullets
        self.bulletCooldown = 0
        self.all_bullets = pygame.sprite.Group()

        # Sound
        self.sound = pygame.mixer.Channel(6)
        self.soundAdversaireAttaque = pygame.mixer.Sound("sounds/AdversaireAttaqué.ogg")
        self.soundAttaquePoliciers = pygame.mixer.Sound('sounds/AttaquePoliciers.ogg')

        # IA
        self.newpos = random.randint(5, 924)
        self.newpos -= self.newpos % self.velocity

        # animation déplacement
        self.walkAnimationRight = False
        self.walkAnimationLeft = False
        self.spritesWalkLeft = [pygame.transform.scale(pygame.image.load('assets/police_def.png'), (160, 160)),
                                pygame.transform.scale(pygame.image.load('assets/police_walk.png'), (160, 160))]
        self.spritesWalkRight = [pygame.transform.flip(self.spritesWalkLeft[0], True, False),
                                pygame.transform.flip(self.spritesWalkLeft[1], True, False)]
        self.walkFrame = 0

        # animation dommage/mort
        self.damaged = False
        self.damagedFrame = 0
        self.spriteDeathLeft = pygame.transform.scale(pygame.image.load('assets/police_death.png'), (160, 160))
        self.spriteDeathRight = pygame.transform.flip(self.spriteDeathLeft, True, False)

    def move(self):
        # randomly move left/right (tolerance of 1 pixel)
        if self.newpos > self.rect.x+1:
            self.right()
        elif self.newpos < self.rect.x-1:
            self.left()
        else :
            self.newpos = random.randint(5, 924)
            self.newpos -= self.newpos % self.velocity
            self.walkAnimationRight = False
            self.walkAnimationLeft = False

    def randomFire(self):
        if(self.bulletCooldown <= 0):
            if(random.random()<0.005):
                self.bulletCooldown = 120 # 2 seconds
                self.sound.play(self.soundAttaquePoliciers,0)
                self.fire()
        else:
            self.bulletCooldown -= 1

    def fire(self):
        self.all_bullets.add(Bullet(self, not(self.facingRight)))

    def right(self):
        self.walkAnimationRight = True
        self.facingRight = True
        self.rect.x += self.velocity

    def left(self):
        self.walkAnimationLeft = True
        self.facingRight = False
        self.rect.x -= self.velocity
        
    def damage(self):
        if(self.health>0):
            self.sound.play(self.soundAdversaireAttaque, 0)
            self.health -= 1
            self.damaged = True
        if(self.health==0):
            self.dead = True
            self.walkAnimationRight = False
            self.walkAnimationLeft = False
            # set sprite to dead
            if(self.facingRight):
                self.currentSprite = self.spriteDeathRight
            else:
                self.currentSprite = self.spriteDeathLeft

    # visual refresh of policier with animations
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
        if(self.damaged):
            self.damagedFrame += 1
            if(self.damaged and self.damagedFrame==37): # stop animation
                self.damaged = False
                self.damagedFrame = 0
                if(self.health==0):
                    self.delete_policier()

        # do the actual update (if we have been hit, skip 1 in 2 frames)
        if (self.damagedFrame%8 < 4):
            screen.blit(self.currentSprite, self.rect)

    def delete_policier(self):
        self.game.all_policiers.remove(self)
        self.game.count_policiers-=1
