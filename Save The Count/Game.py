import pygame
from Jack import Player
from Policier import Policier
from Policier_matraque import Matraque
from Senator import SenatorBlue
from Senator import SenatorRed


class Game:
    def __init__(self, hud):
        self.playing = False

        # Jack
        self.player = Player(hud, self)
        self.hud = hud
        self.pressed = {}
        self.level = [True, False, False, False, False]

        # Policiers
        self.all_policiers = pygame.sprite.Group()
        self.all_matraque = pygame.sprite.Group()
        self.count_policiers = 0

        # Sénateurs
        self.all_senblue = pygame.sprite.Group()
        self.all_senred = pygame.sprite.Group()
        self.count_senator_blue = 0
        self.count_senator_red = 0

    def spawn_policier(self, x):
        self.count_policiers += x
        while x > 0:
            policier = Policier(self)
            self.all_policiers.add(policier)
            x -= 1


    def spawn_matraque(self, x):
        self.count_policiers += x
        while x > 0:
            matraque = Matraque(self)
            self.all_matraque.add(matraque)
            x -= 1

    def spawn_senator_blue(self, x):
        self.count_senator_blue += x
        while x > 0:
            senblue = SenatorBlue(self)
            self.all_senblue.add(senblue)
            x -= 1


    def spawn_senator_red(self, x):
        self.count_senator_red += x
        while x > 0:
            senred = SenatorRed(self)
            self.all_senred.add(senred)
            x -= 1

