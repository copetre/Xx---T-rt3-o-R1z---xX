import pygame
from Jack import Player

class Game:

    def __init__(self, screen, hud):
        # Jack
        self.player = Player(screen, hud)
        self.pressed = {}