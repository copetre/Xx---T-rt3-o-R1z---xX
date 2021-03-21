import pygame

class HUD:
    def __init__(self):
        # attributes
        self.maxHealth = 3
        self.health = self.maxHealth

        # Hearts
        self.hearts = []
        for i in range(self.maxHealth):
            self.hearts.append(Heart(i))

        # Votebar
        self.votebar = VoteBar()
    
    # function to call to refresh the hud constantly
    def refresh(self, screen):
        # update hearts
        for i in range(len(self.hearts)):
            self.hearts[i].refresh(screen)

        # update bar
        self.votebar.refresh(screen)

    def loseHeart(self):
        if(self.health>0):
            # set inactive only after animation
            self.hearts[self.health-1].blinkingAnimationLose=True
            self.health = self.health-1

    def healHeart(self):
        if(self.health<self.maxHealth):
            # set active immediately
            self.hearts[self.health].active=True
            self.hearts[self.health].blinkingAnimationHeal=True
            self.health = self.health+1

class Heart:
    # index = indicates which heart it is (0, 1, 2)
    def __init__(self, index):
        # attributes
        self.index = index
        self.active = True

        # animation
        self.blinkingAnimationLose = False
        self.blinkingAnimationHeal = False
        self.blinkingFrame = 0

        # heart surface
        self.image = pygame.image.load('asset/HEART.png')
        self.background = self.image.get_rect(center = (48 * (self.index+1) - 16, 32))

    # function to call to refresh the heart constantly
    def refresh(self, screen):
        # if supposed to be blinking
        if(self.blinkingAnimationLose):
            self.blinkingFrame += 1
            if (self.blinkingFrame == 36):  # stop animation
                self.blinkingAnimationLose = False
                self.active = False
                self.blinkingFrame = 0
        elif(self.blinkingAnimationHeal):
            self.blinkingFrame += 1
            if (self.blinkingFrame == 36):  # stop animation
                self.blinkingAnimationHeal = False
                self.blinkingFrame = 0

        # only refresh if active (=not lost), with blinking animation if necessary
        if(self.active and self.blinkingFrame % 8 < 4):
            screen.blit(self.image, self.background)

class VoteBar:
    def __init__(self):
        # attributes
        self.font = pygame.freetype.Font("asset/unispace bd.ttf", 24)
        self.redPercent = 5
        self.bluePercent = 5

        # animation
        self.redDecreaseAnimation = False
        self.blueDecreaseAnimation = False
        self.redDecreaseFrame = 0
        self.blueDecreaseFrame = 0

        # background surface
        self.surface = pygame.Surface((800, 32))
        self.surface.fill((128, 128, 128))
        self.background = self.surface.get_rect(left = 208, top = 16) # alternative = (center = (608, 32))

        # separation bar
        self.surfaceSeparation = pygame.Surface((2, 48))
        self.surfaceSeparation.fill((0, 0, 0))
        self.backgroundSeparation = self.surfaceSeparation.get_rect(center = (608, 32)) # alternative = (center = (608, 32))
    
    # increases red percentage by 1, without exceeding max
    def redInc(self):
        if(self.redPercent<100-self.bluePercent):
            self.redPercent = self.redPercent+1
    
    # increases blue percentage by 1, without exceeding max
    def blueInc(self):
        if(self.bluePercent<100-self.redPercent):
            self.bluePercent = self.bluePercent+1

    # decrease red percentage by 4 (senators), without going under 2
    def redDes(self):
        if (self.redPercent>0):
            self.redPercent = max(self.redPercent-4, 2)
            self.redDecreaseAnimation = True

    # decrease blue percentage by 4 (senators), without going under 2
    def blueDes(self):
        if (self.bluePercent>0):
            self.bluePercent = max(self.bluePercent-4, 2)
            self.blueDecreaseAnimation = True

    # function to call to refresh the votebar constantly
    def refresh(self, screen):
        # background surface
        screen.blit(self.surface, self.background)

        # if flashing bar(s)
        if (self.redDecreaseAnimation):
            self.redDecreaseFrame += 1
            if (self.redDecreaseFrame == 36):  # stop animation
                self.redDecreaseAnimation = False
                self.redDecreaseFrame = 0
        if (self.blueDecreaseAnimation):
            self.blueDecreaseFrame += 1
            if (self.blueDecreaseFrame == 36):  # stop animation
                self.blueDecreaseAnimation = False
                self.blueDecreaseFrame = 0

        # red surface
        if (self.redDecreaseFrame % 8 < 4):
            self.surfaceRed = pygame.Surface((self.redPercent * 8, 32))
            self.surfaceRed.fill((255, 0, 0))
            self.backgroundRed = self.surfaceRed.get_rect(left = 208, top = 16)
            screen.blit(self.surfaceRed, self.backgroundRed)

        # blue surface
        if (self.blueDecreaseFrame % 8 < 4):
            self.surfaceBlue = pygame.Surface((self.bluePercent * 8, 32))
            self.surfaceBlue.fill((0, 0, 255))
            self.backgroundBlue = self.surfaceBlue.get_rect(right = 1008, top = 16)
            screen.blit(self.surfaceBlue, self.backgroundBlue)

        # separe surface
        screen.blit(self.surfaceSeparation, self.backgroundSeparation)

        # txt elector
        textSurfaceRed, textRectRed = self.font.render(str(round(self.redPercent*5.38)), (0, 0, 0))
        textRectRed.left=216
        textRectRed.top=24
        textSurfaceBlue, textRectBlue = self.font.render(str(round(self.bluePercent*5.38)), (0, 0, 0))
        textRectBlue.right = 1000
        textRectBlue.top=24
        screen.blit(textSurfaceRed, textRectRed)
        screen.blit(textSurfaceBlue, textRectBlue)
        textSurfaceElecteurs, textRectElecteurs = self.font.render("Voters", (0, 0, 0))
        screen.blit(textSurfaceElecteurs, (608-textRectElecteurs.width//2, 64))