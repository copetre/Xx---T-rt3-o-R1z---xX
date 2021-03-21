import pygame
import random

class SenatorBlue(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        # pygame
        self.game = game

        # attributes
        self.health = 1
        self.max_health = 1
        self.velocity = 2
        self.dead = False

        # senator box
        self.size = 160 + random.randint(-20, 20)
        self.currentSprite = pygame.transform.scale(pygame.image.load('assets/senator_def_blue.png'), (160, self.size))
        self.rect = self.currentSprite.get_rect()
        self.rect.x = 80 * random.randint(3, 10)
        self.rect.y = 380 + random.randint(-10, 10)
        self.groundY = self.rect.y
        self.facingRight = False

        # Sound
        self.sound = pygame.mixer.Channel(3)
        self.soundAdversaireAttaque = pygame.mixer.Sound("sounds/AdversaireAttaqué.ogg")

        # IA
        self.newpos = random.randint(5, 924)
        self.newpos -= self.newpos % self.velocity

        # jump
        self.jumping = False
        self.jumpingVelocity = 0

        # animation déplacement
        self.walkAnimationRight = False
        self.walkAnimationLeft = False
        self.spritesWalkLeft = [pygame.transform.scale(pygame.image.load('assets/senator_def_blue.png'), (160, self.size)),
                                pygame.transform.scale(pygame.image.load('assets/senator_walk_blue.png'), (160, self.size))]
        self.spritesWalkRight = [pygame.transform.flip(self.spritesWalkLeft[0], True, False),
                                 pygame.transform.flip(self.spritesWalkLeft[1], True, False)]
        self.walkFrame = 0

        # animation déplacement + scared
        self.scared = False
        self.spritesWalkLeftScared = [pygame.transform.scale(pygame.image.load('assets/senator_scared_blue.png'), (160, self.size)),
                                      pygame.transform.scale(pygame.image.load('assets/senator_scared_walk_blue.png'), (160, self.size))]
        self.spritesWalkRightScared = [pygame.transform.flip(self.spritesWalkLeftScared[0], True, False),
                                       pygame.transform.flip(self.spritesWalkLeftScared[1], True, False)]
        self.walkFrame = 0

        # animation dommage/mort
        self.damaged = False
        self.damagedFrame = 0
        self.spriteDeathLeft = pygame.transform.scale(pygame.image.load('assets/senator_death_blue.png'), (160, self.size))
        self.spriteDeathRight = pygame.transform.flip(self.spriteDeathLeft, True, False)

    def move(self):
        # randomly move left/right (tolerance of 1 pixel)
        if self.newpos > self.rect.x+1:
            self.right()
        elif self.newpos < self.rect.x-1:
            self.left()
        else:
            self.newpos = random.randint(5, 924)
            self.newpos -= self.newpos % self.velocity
            self.walkAnimationRight = False
            self.walkAnimationLeft = False
        # if scared, jump randomly
        if(self.scared and random.random() < 0.025):
            self.jump()

    def right(self):
        self.walkAnimationRight = True
        self.facingRight = True
        self.rect.x += self.velocity

    def left(self):
        self.walkAnimationLeft = True
        self.facingRight = False
        self.rect.x -= self.velocity

    def jump(self):
        # only jumps if on ground
        if (self.rect.y == self.groundY):
            self.jumping = True
            self.jumpingVelocity = 12

    def gravity(self):
        # if we are jumping, continue going upwards
        if (self.jumping):
            # move upwards
            self.rect.y = min(self.rect.y - self.jumpingVelocity, self.groundY)

            # decrease y-velocity
            self.jumpingVelocity = self.jumpingVelocity - 0.5 
            
            if (self.rect.y == self.groundY):
                #if on the ground, stop
                self.jumping = False
                self.jumpingVelocity = 0

    def damage(self):
        if (self.health > 0):
            self.sound.play(self.soundAdversaireAttaque, 0)
            self.health -= 1
            self.damaged = True
        if (self.health == 0):
            self.dead = True
            self.walkAnimationRight = False
            self.walkAnimationLeft = False
            # set sprite to dead
            if(self.facingRight):
                self.currentSprite = self.spriteDeathRight
            else:
                self.currentSprite = self.spriteDeathLeft
            # update hud
            self.game.hud.votebar.blueDes()

    # visual refresh of blue senator with animations
    def refresh(self, screen):
        # if walking in any direction, increase frame
        if (self.walkAnimationLeft or self.walkAnimationRight):
            self.walkFrame = (self.walkFrame + 1) % 12  # %12 because we have 2 frames * 6 ticks each

        # set current sprite
        if not(self.scared):
            if (self.walkAnimationLeft):
                self.currentSprite = self.spritesWalkLeft[self.walkFrame // 6]  # //6 because update every 6 ticks
            elif (self.walkAnimationRight):
                self.currentSprite = self.spritesWalkRight[self.walkFrame // 6]  # //6 because update every 6 ticks
        else:
            if (self.walkAnimationLeft):
                self.currentSprite = self.spritesWalkLeftScared[self.walkFrame // 6]  # //6 because update every 6 ticks
            elif (self.walkAnimationRight):
                self.currentSprite = self.spritesWalkRightScared[self.walkFrame // 6]  # //6 because update every 6 ticks

        # if we've been damaged, increase damaged frame (same if we are dead)
        if (self.damaged):
            self.damagedFrame += 1
            if (self.damaged and self.damagedFrame == 37):  # stop animation
                self.damaged = False
                self.damagedFrame = 0
                if (self.health == 0):
                    self.delete_senator()

        # do the actual update (if we have been hit, skip 1 in 2 frames)
        if (self.damagedFrame % 8 < 4):
            screen.blit(self.currentSprite, self.rect)

    def delete_senator(self):
        self.game.all_senblue.remove(self)
        self.game.count_senator_blue -= 1

class SenatorRed(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        # pygame
        self.game = game

        # attributes
        self.health = 1
        self.max_health = 1
        self.velocity = 2
        self.dead = False
        self.size = 160 + random.randint(-20,20)

        # senator box
        self.currentSprite = pygame.transform.scale(pygame.image.load('assets/senator_def_red.png'), (160, self.size))
        self.rect = self.currentSprite.get_rect()
        self.rect.x = 80 * random.randint(3, 10)
        self.rect.y = 380 + random.randint(-10, 10)
        self.groundY = self.rect.y
        self.facingRight = False

        # Sound
        self.sound = pygame.mixer.Channel(4)
        self.soundAdversaireAttaque = pygame.mixer.Sound("sounds/AdversaireAttaqué.ogg")

        # IA
        self.newpos = random.randint(5, 924)
        self.newpos -= self.newpos % self.velocity
        
        # jump
        self.jumping = False
        self.jumpingVelocity = 0

        # animation déplacement
        self.walkAnimationRight = False
        self.walkAnimationLeft = False
        self.spritesWalkLeft = [pygame.transform.scale(pygame.image.load('assets/senator_def_red.png'), (160, self.size)),
                                pygame.transform.scale(pygame.image.load('assets/senator_walk_red.png'), (160, self.size))]
        self.spritesWalkRight = [pygame.transform.flip(self.spritesWalkLeft[0], True, False),
                                 pygame.transform.flip(self.spritesWalkLeft[1], True, False)]
        self.walkFrame = 0

        # animation déplacement + scared
        self.scared = False
        self.spritesWalkLeftScared = [pygame.transform.scale(pygame.image.load('assets/senator_scared_red.png'), (160, self.size)),
                                      pygame.transform.scale(pygame.image.load('assets/senator_scared_walk_red.png'), (160, self.size))]
        self.spritesWalkRightScared = [pygame.transform.flip(self.spritesWalkLeftScared[0], True, False),
                                       pygame.transform.flip(self.spritesWalkLeftScared[1], True, False)]
        self.walkFrame = 0

        # animation dommage/mort
        self.damaged = False
        self.damagedFrame = 0
        self.spriteDeathLeft = pygame.transform.scale(pygame.image.load('assets/senator_death_red.png'), (160, self.size))
        self.spriteDeathRight = pygame.transform.flip(self.spriteDeathLeft, True, False)

    def move(self):
        # randomly move left/right (tolerance of 1 pixel)
        if self.newpos > self.rect.x+1:
            self.right()
        elif self.newpos < self.rect.x-1:
            self.left()
        else:
            self.newpos = random.randint(5, 924)
            self.newpos -= self.newpos % self.velocity
            self.walkAnimationRight = False
            self.walkAnimationLeft = False
        # if scared, jump randomly
        if(self.scared and random.random() < 0.025):
            self.jump()

    def right(self):
        self.walkAnimationRight = True
        self.facingRight = True
        self.rect.x += self.velocity

    def left(self):
        self.walkAnimationLeft = True
        self.facingRight = False
        self.rect.x -= self.velocity

    def jump(self):
        # only jumps if on ground
        if (self.rect.y == self.groundY):
            self.jumping = True
            self.jumpingVelocity = 12

    def gravity(self):
        # if we are jumping, continue going upwards
        if (self.jumping):
            # move upwards
            self.rect.y = min(self.rect.y - self.jumpingVelocity, self.groundY)

            # decrease y-velocity
            self.jumpingVelocity = self.jumpingVelocity - 0.5 
            
            if (self.rect.y == self.groundY):
                #if on the ground, stop
                self.jumping = False
                self.jumpingVelocity = 0

    def damage(self):
        if (self.health > 0):
            self.sound.play(self.soundAdversaireAttaque,0)
            self.health -= 1
            self.damaged = True
        if (self.health == 0):
            self.dead = True
            self.walkAnimationRight = False
            self.walkAnimationLeft = False
            # set sprite to dead
            if(self.facingRight):
                self.currentSprite = self.spriteDeathRight
            else:
                self.currentSprite = self.spriteDeathLeft
            # update hud
            self.game.hud.votebar.redDes()

    # visual refresh of blue senator with animations
    def refresh(self, screen):
        # if walking in any direction, increase frame
        if (self.walkAnimationLeft or self.walkAnimationRight):
            self.walkFrame = (self.walkFrame + 1) % 12  # %12 because we have 2 frames * 6 ticks each
        
        # set current sprite
        if not(self.scared):
            if (self.walkAnimationLeft):
                self.currentSprite = self.spritesWalkLeft[self.walkFrame // 6]  # //6 because update every 6 ticks
            elif (self.walkAnimationRight):
                self.currentSprite = self.spritesWalkRight[self.walkFrame // 6]  # //6 because update every 6 ticks
        else:
            if (self.walkAnimationLeft):
                self.currentSprite = self.spritesWalkLeftScared[self.walkFrame // 6]  # //6 because update every 6 ticks
            elif (self.walkAnimationRight):
                self.currentSprite = self.spritesWalkRightScared[self.walkFrame // 6]  # //6 because update every 6 ticks

        # if we've been damaged, increase damaged frame (same if we are dead)
        if (self.damaged):
            self.damagedFrame += 1
            if (self.damaged and self.damagedFrame == 37):  # stop animation
                self.damaged = False
                self.damagedFrame = 0
                if (self.health == 0):
                    self.delete_senator()

        # do the actual update (if we have been hit, skip 1 in 2 frames)
        if (self.damagedFrame % 8 < 4):
            screen.blit(self.currentSprite, self.rect)

    def delete_senator(self):
        self.game.all_senred.remove(self)