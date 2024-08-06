import pygame
import random
import GUIs.inventoryUIs as inventory

# this file will return the following output:
#
# the health,stamina and mana bar positions and sizes, colours and the amount of health, stamina and mana the player has
# this data should be taken directly from the player object attributes in the Game class.(so game.player.attrs)

# refer to loose projects file for the full code for the health bar.

# target hp, which it shrinks to each frame


class HealthBar:

    def __init__(self, player, screen):

        self.x_pos, self.y_pos = screen.get_size()[0]*0.1, 2

        self.width = screen.get_size()[0]*0.3

        self.height = screen.get_size()[1]*0.02

        self.player = player

        self.targetHP = self.player.HP

        self.screen = screen

    def draw(self):

        self.player.HP = min(max(self.player.HP, 0), self.player.maxHP)
        self.targetHP = min(self.targetHP, self.player.maxHP)

        self.updateTargetHP()
        #self.targetHP = self.player.HP

        # First, draw a black background for the health bar that is 2 pixels greater in each direction than the health bar itself

        pygame.draw.rect(self.screen, (0, 0, 0), (self.x_pos-2, self.y_pos-2, self.width+4, self.height+4))

        # Then, draw the health bar itself, with its width depending on the player's current health

        pygame.draw.rect(self.screen, (255, 0, 0), (self.x_pos, self.y_pos, self.width*(self.targetHP/self.player.maxHP), self.height))

    def updateTargetHP(self):

        # This function will be called every frame to update the targetHP value

        if self.targetHP > self.player.HP:

            self.targetHP -= 1

        elif self.targetHP < self.player.HP:

            self.targetHP += 1

        else:

            self.targetHP = self.player.HP



class ManaBar:

    def __init__(self, player, screen):

        self.x_pos, self.y_pos = screen.get_size()[0]*0.1, 4 + screen.get_size()[1]*0.02

        self.width = screen.get_size()[0]*0.25

        self.height = screen.get_size()[1]*0.02

        self.player = player

        self.screen = screen

    def draw(self):

        # First, draw a black background for the mana bar that is 2 pixels greater in each direction than the mana bar itself

        pygame.draw.rect(self.screen, (0, 0, 0), (self.x_pos-2, self.y_pos-2, self.width+4, self.height+4))

        # Then, draw the mana bar itself, with its width depending on the player's current mana

        pygame.draw.rect(self.screen, (0, 0, 255), (self.x_pos, self.y_pos, self.width*(self.player.mana/self.player.maxMana), self.height))


class StaminaBar:

    def __init__(self, player, screen):

        self.x_pos, self.y_pos = screen.get_size()[0]*0.1, 6 + screen.get_size()[1]*0.04

        self.width = screen.get_size()[0]*0.2

        self.height = screen.get_size()[1]*0.02

        self.player = player

        self.screen = screen

    def draw(self):

        # First, draw a black background for the stamina bar that is 2 pixels greater in each direction than the stamina bar itself

        pygame.draw.rect(self.screen, (0, 0, 0), (self.x_pos-2, self.y_pos-2, self.width+4, self.height+4))

        # Then, draw the stamina bar itself, with its width depending on the player's current stamina

        pygame.draw.rect(self.screen, (255, 255, 255), (self.x_pos, self.y_pos, self.width*(self.player.stamina/self.player.maxStamina), self.height))

        #  Pygame documentation website is a good resource for learning how to use the pygame library
        # URL : https://www.pygame.org/docs/
class GUI:

    def __init__(self, player, screen, images, font):

        self.frames = 0

        self.health_bar = HealthBar(player, screen)

        self.stamina_bar = StaminaBar(player, screen)

        self.mana_bar = ManaBar(player, screen)

        self.font = font

        self.inventory_ui = inventory.InventoryUI(player, screen, images, font)

        self.player = player

    def drawUIs(self):  # Called every frame

        self.frames += 1

        self.health_bar.draw()

        self.stamina_bar.draw()

        self.mana_bar.draw()

    def drawInventory(self):

        self.inventory_ui.draw()

    def inventoryClick(self, mouse_pos):
        for slot in inventory.InventorySlot.slots:
            slot.clicked(mouse_pos)

        for button in inventory.InventoryButton.buttons:
            button.clicked(mouse_pos, self.player)

        for slot in self.inventory_ui.equipment_slots['slots']:
            slot.clicked(mouse_pos, self.player)

    def unselectInventorySlot(self):
        inventory.InventorySlot.unselect()
