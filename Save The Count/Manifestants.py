import pygame
import random


class Manifestant(pygame.sprite.Sprite):

    def __init__(self, game, type):
        super().__init__()
        # pygame
        self.game = game

        # attributes
        self.health = 1
        self.max_health = 1
        self.velocity = 2
        self.size = 160 + random.randint(-20, 20)
        self.dead = False

        # Type of manifestant

        if (type == 1):
            self.currentSprite = pygame.transform.scale(pygame.image.load('asset/mob_def_1.png'), (160, self.size))
        elif (type == 2):
            self.currentSprite = pygame.transform.scale(pygame.image.load('asset/mob_def_2.png'), (160, self.size))
        elif (type == 3):
            self.currentSprite = pygame.transform.scale(pygame.image.load('asset/mob_def_3.png'), (160, self.size))

        # manifestants box

        self.rect = self.currentSprite.get_rect()
        self.rect.x = 50
        self.rect.y = 380 + random.randint(-10, 10)
        self.groundY = self.rect.y
        self.sound = pygame.mixer.Channel(3)
        self.facingRight = False


        # IA
        self.newpos = random.randint(5, 924)
        self.newpos -= self.newpos % self.velocity

        # jump
        self.jumping = True
        self.jumpingVelocity = 0

        # animation déplacement
        self.walkAnimationRight = False
        self.walkAnimationLeft = False
        if (type == 1):
            self.spritesWalkLeft = [
                pygame.transform.scale(pygame.image.load('asset/mob_def_1.png'), (160, self.size)),
                pygame.transform.scale(pygame.image.load('asset/mob_walk_1.png'), (160, self.size))]
        elif (type == 2):
            self.spritesWalkLeft = [
                pygame.transform.scale(pygame.image.load('asset/mob_def_2.png'), (160, self.size)),
                pygame.transform.scale(pygame.image.load('asset/mob_walk_2.png'), (160, self.size))]
        elif (type == 3):
            self.spritesWalkLeft = [
                pygame.transform.scale(pygame.image.load('asset/mob_def_3.png'), (160, self.size)),
                pygame.transform.scale(pygame.image.load('asset/mob_walk_3.png'), (160, self.size))]

        self.spritesWalkRight = [pygame.transform.flip(self.spritesWalkLeft[0], True, False),
                                 pygame.transform.flip(self.spritesWalkLeft[1], True, False)]
        self.walkFrame = 0



    def move(self):
        # randomly move left/right (tolerance of 1 pixel)
        if self.newpos > self.rect.x + 1:
            self.right()
        elif self.newpos < self.rect.x - 1:
            self.left()
        else:
            self.newpos = random.randint(5, 924)
            self.newpos -= self.newpos % self.velocity
            self.walkAnimationRight = False
            self.walkAnimationLeft = False
        #jump randomly
        if random.random() < 0.2:
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
                # if on the ground, stop
                self.jumping = False
                self.jumpingVelocity = 0

    # visual refresh of blue senator with animations
    def refresh(self, screen):
        # if walking in any direction, increase frame
        if (self.walkAnimationLeft or self.walkAnimationRight):
            self.walkFrame = (self.walkFrame + 1) % 12  # %12 because we have 2 frames * 6 ticks each

        # set current sprite
        if (self.walkAnimationRight):
            self.currentSprite = self.spritesWalkLeft[self.walkFrame // 6]  # //6 because update every 6 ticks
        elif (self.walkAnimationLeft):
            self.currentSprite = self.spritesWalkRight[self.walkFrame // 6]  # //6 because update every 6 ticks

        screen.blit(self.currentSprite, self.rect)


    def delete_manifestant(self):
        self.game.all_manifestants.remove(self)
        self.game.count_manifestants -= 1
