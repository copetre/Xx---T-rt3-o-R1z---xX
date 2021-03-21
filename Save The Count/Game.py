import pygame
import pygame.freetype  # for fonts
import random
from Jack import Player
from Policier import Policier
from Policier_matraque import Matraque
from Senator import SenatorBlue
from Senator import SenatorRed
from Manifestants import Manifestant


class Game:
    def __init__(self, hud):
        # Death
        self.playing = False
        self.gameOverFrame = 0
        self.win = False
        self.lose = False
        self.increaseRedOdds = False
        self.gotRoomHealAlready = True # true par défaut, false si on fait spawn des bleus

        # Jack
        self.player = Player(hud, self)
        self.hud = hud
        self.pressed = {}
        self.level = [True, False, False, False, False, False, False]

        # Policiers
        self.all_policiers = pygame.sprite.Group()
        self.all_matraque = pygame.sprite.Group()
        self.count_policiers = 0

        # Sénateurs
        self.all_senblue = pygame.sprite.Group()
        self.all_senred = pygame.sprite.Group()
        self.count_senator_blue = 0
        self.count_senator_red = 0

        # Manifestants
        self.all_manifestants = pygame.sprite.Group()
        self.count_manifestants = 0

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

    def spawn_manifestants(self, x):
        self.count_manifestants += x
        while x > 0:
            mani = Manifestant(self, random.randint(1, 3))
            self.all_manifestants.add(mani)
            x -= 1

    def delete_senator_blue(self, senblue):
        senblue.delete_senator()

    def delete_senator_red(self, senred):
        senred.delete_senator()

    def delete_matraque(self, matraque):
        matraque.delete_policier()

    def delete_policier(self, policier):
        policier.delete_policier()

    def delete_manifestant(self, manifestant):
        manifestant.delete_manifestant()
