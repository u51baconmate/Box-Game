"""
This file should contain the GUI for fighting. This involves the spell and skill slots,
Health Bar, Mana Bar, Stamina Bar, and Enemy Health Bar.

Animations are not compatible with the current version of the game, so they will not be included.

TODO: Complete Fighting GUI.


"""

import pygame
import GUIs.icons as icons
import numpy as np
import math

#  import numpy as np # might be useful for animations


class FightingGUI:

    def __init__(self, player, screen, enemy, frame):

        self.player = player
        self.screen = screen
        self.enemy = enemy
        self.frame = frame

        self.inAnim = False

    def initiateFight(self):
        self.inAnim = True
        # in this function, call fade to black and display and spin the enemy sprite
        self.fadeToBlack()

        self.inAnim = False

    def fadeToBlack(self):

        fight = pygame.image.load("GUIs/Icons/fight.png")

        fade = pygame.Surface((self.screen.get_size()))
        fade.fill((0, 0, 0))

        rotation_angle = 180

        for alpha in range(0, 240):

            if alpha > 200:
                alpha = 200

            fade.set_alpha(alpha//6)
            self.screen.blit(fade, (0, 0))
            pygame.time.delay(20)

            # rotate fight by sin(alpha)
            rotation_angle += 2 if rotation_angle < 360 else 0
            rotated_fight = pygame.transform.rotate(fight, rotation_angle)
            scaled_fight = pygame.transform.scale(rotated_fight, (alpha*4, alpha*4))
            self.screen.blit(scaled_fight, (self.screen.get_size()[0]//2 - alpha*2, self.screen.get_size()[1]//2 - alpha*2))

            pygame.display.flip()









    def drawHealthBar(self):
        pass

    def drawManaBar(self):
        pass

    def drawStaminaBar(self):
        pass



