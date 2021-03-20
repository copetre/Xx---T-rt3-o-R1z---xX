import pygame

class HUD:
    # screen = the pygame screen to draw on
    def __init__(self, screen):
        # attributes
        self.screen = screen
        self.maxHealth = 3
        self.health = self.maxHealth

        # HUD surface
        # self.surface = pygame.Surface((1024, 64))
        # self.surface.fill((128, 128, 128))
        # self.background = self.surface.get_rect()

        # Hearts
        self.hearts = []
        for i in range(self.maxHealth):
            self.hearts.append(Heart(screen, i))

        # Votebar
        self.votebar = VoteBar(screen)
    
    # function to call to refresh the hud constantly
    def refresh(self):
        # update HUD background
        # self.screen.blit(self.surface, self.background)

        # update hearts
        for i in range(len(self.hearts)):
            self.hearts[i].refresh()

        # update bar
        self.votebar.refresh()

    def loseHeart(self):
        if(self.health>0):
            self.hearts[self.health-1].active=False
            self.health = self.health-1

    def healHeart(self):
        if(self.health<self.maxHealth):
            self.hearts[self.health].active=True
            self.health = self.health+1

class Heart:
    # screen = the pygame screen to draw on
    # index = indicates which heart it is (0, 1, 2)
    def __init__(self, screen, index):
        # attributes
        self.screen = screen
        self.index = index
        self.active = True

        # heart surface
        self.image = pygame.image.load('asset/HEART.png')
        self.background = self.image.get_rect(center = (48 * (self.index+1) - 16, 32))
        screen.blit(self.image, self.background)

    # function to call to refresh the heart constantly
    def refresh(self):
        if(self.active): # only refresh if active (=not lost)
            self.screen.blit(self.image, self.background)

class VoteBar:
    # screen = the pygame screen to draw on
    def __init__(self, screen):
        # attributes
        self.screen = screen
        self.redPercent = 0
        self.bluePercent = 0

        # background surface
        self.surface = pygame.Surface((800, 32))
        self.surface.fill((128, 128, 128))
        self.background = self.surface.get_rect(left = 208, top = 16) # alternative = (center = (608, 32))

        # separation bar
        self.surfaceSeparation = pygame.Surface((2, 48))
        self.surfaceSeparation.fill((0, 0, 0))
        self.backgroundSeparation = self.surfaceSeparation.get_rect(center = (608, 32)) # alternative = (center = (608, 32))
        
        self.refresh()
    
    # increases red percentage by 1, without exceeding max
    def redInc(self):
        if(self.redPercent<100-self.bluePercent):
            self.redPercent = self.redPercent+1
    
    # increases blue percentage by 1, without exceeding max
    def blueInc(self):
        if(self.bluePercent<100-self.redPercent):
            self.bluePercent = self.bluePercent+1

    # function to call to refresh the votebar constantly
    def refresh(self):
        # background surface
        self.screen.blit(self.surface, self.background)

        # separation surface
        self.screen.blit(self.surfaceSeparation, self.backgroundSeparation)

        # red surface
        self.surfaceRed = pygame.Surface((self.redPercent * 8, 32))
        self.surfaceRed.fill((255, 0, 0))
        self.backgroundRed = self.surfaceRed.get_rect(left = 208, top = 16)
        self.screen.blit(self.surfaceRed, self.backgroundRed)

        # blue surface
        self.surfaceBlue = pygame.Surface((self.bluePercent * 8, 32))
        self.surfaceBlue.fill((0, 0, 255))
        self.backgroundBlue = self.surfaceBlue.get_rect(right = 1008, top = 16)
        self.screen.blit(self.surfaceBlue, self.backgroundBlue)