import sys

import pygame
import Configs.Configs as Configs
import time
import random

#  This code was thrown together in order to create the config page. It is not meant to be
#  Efficient, and is not a good example of programming practice or style. It is simply a
#  way for players to decide some settings before they load the game.


class ControlsText:

    #  Literally just a text box that displays the controls. It is not interactive (yet)
    #  To add keybinds in the future, just make a dict with the keyboard letter and value associated with it.

    def __init__(self, screen, x, y, width, height, text, font_size):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw()

    def draw(self):
        self.screen.blit(self.font.render(self.text, True, (0, 0, 0)), (self.x, self.y))


class ConfigValueBox:  # The value box displays the value from the config value, and when clicked, allows the user to change it.

    font = None

    boxes = []

    currentTarget = None

    def __init__(self, screen, x, y, width, height, _class, value, description):

        self.page = "config"
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = getattr(_class, value)
        self.valueName = value
        self.text = ConfigValueBox.font.render(value, True, (0, 0, 0))
        self.description = ConfigValueBox.font.render(description, True, (0, 0, 0))
        self.awaitingInput = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        ConfigValueBox.boxes.append(self)
        self.draw()

    def click(self, typeCall):

        if typeCall == "click":
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.awaitingInput = True
                ConfigValueBox.currentTarget = self
                ConfigValueBox.disableOther()

    def change(self):
        setattr(Configs.Configs, self.valueName, self.value)

    def draw(self):
        self.text = ConfigValueBox.font.render(str(self.value), True, (0, 0, 0))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x-1, self.y-1, self.width+2, self.height+2))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
        self.screen.blit(self.text, (self.x + self.width / 2 - self.text.get_width() / 2, self.y + self.height / 2 - self.text.get_height() / 2))
        self.screen.blit(self.description, (self.x + self.width + 10, self.y + self.height / 2 - self.description.get_height() / 2))

    def inputText(self, text):
        try:
            if text == "BACKSPACE" and len(str(self.value)) > 1:
                self.value = int(str(self.value)[:-1])
            elif text == "BACKSPACE":
                self.value = 0
            elif text is not None:
                self.value = int(str(self.value) + str(text))
        except (ValueError, TypeError):
            pass

        self.change()

    @classmethod
    def disableOther(cls):
        for box in cls.boxes:
            if box != cls.currentTarget:
                box.awaitingInput = False


class ConfigToggles:

    font = None

    def __init__(self, screen, x, y, width, height, _class, value, side_text):
        self.page = "config"
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = getattr(Configs.Configs, value)

        self.setType = type(self.value)

        if self.value == "Auto":
            self.value = True
        else:
            self.value = False

        self.valueName = value

        self.text = ConfigToggles.font.render(side_text, True, (0, 0, 0))

        if self.value and self.value != 'Custom':
            self.colour = (0, 255, 0)
        else:
            self.colour = (255, 0, 0)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw()

    def draw(self):

        # Create a black rectangle as the background for the toggle

        pygame.draw.rect(self.screen, (0, 0, 0), (self.x-1, self.y-1, self.width+2, self.height+2))

        pygame.draw.rect(self.screen, self.colour, self.rect)
        self.screen.blit(self.text, (self.x + self.width + 10, self.y + self.height / 2 - self.text.get_height() / 2))

    def click(self):

        if self.rect.collidepoint(pygame.mouse.get_pos()):

            if self.colour == (0, 255, 0):

                self.colour = (255, 0, 0)
                self.value = False

            else:
                self.colour = (0, 255, 0)
                self.value = True

        if self.setType is bool:
            setattr(Configs.Configs, self.valueName, self.value)

        elif self.setType is str:
            setattr(Configs.Configs, self.valueName, "Auto" if self.value else "Custom")

        elif self.valueName == "seed":
            if self.value:
                setattr(Configs.Configs, self.valueName, random.randint(0, 50000))
            else:
                setattr(Configs.Configs, self.valueName, 7440)  # 7400 Is the default Custom Config seed

    def updateColour(self):
        if self.value:
            self.colour = (0, 255, 0)
        else:
            self.colour = (255, 0, 0)



class ConfigButtons:

    def __init__(self, screen, x, y, width, height, text, font_size, colour, hover_colour, action, page, target):
        self.page = page
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, font_size)
        self.text = self.font.render(text, True, (0, 0, 0))
        self.colour = colour
        self.hover_colour = hover_colour
        self.action = action
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.target = target
        self.draw()

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, self.rect)
        self.screen.blit(self.text, (self.x + self.width / 2 - self.text.get_width() / 2, self.y + self.height / 2 - self.text.get_height() / 2))

    def click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.action is not None:
                if self.target is not None:
                    self.action(self.target)
                else:
                    self.action()
            else:
                Configs.Configs.current_page = self.page
            return True
        return False


class ConfigScreen:

    def __init__(self):

        self.setStandardConfigs()
        print("Standard Configs Set")

        pygame.init()

        pygame.display.set_caption("Box Game Configuration and Setup - Main Screen")

        ConfigToggles.font = pygame.font.Font(None, 24)
        ConfigValueBox.font = pygame.font.Font(None, 24)

        self.screen = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.running = True
        self.title = pygame.image.load("Configs/config_title.png")
        self.title = pygame.transform.scale(self.title, (600, 400))
        self.page = "menu"
        self.timeSinceChange = time.time()-10

        self.buttons = []
        self.buttons.append(ConfigButtons(self.screen, 50, 400, 200, 50, "Start Standard", 32, (0, 255, 0), (128, 128, 128), self.start_game, "menu", None))
        self.buttons.append(ConfigButtons(self.screen, 300, 400, 260, 50, "Standard - No Map Load", 32, (0, 255, 0), (128, 128, 128), self.start_noMap, "menu", None))
        self.buttons.append(ConfigButtons(self.screen, 50, 500, 200, 50, "Custom Configs", 24, (0, 255, 0), (128, 128, 128), self.change_page, "menu", "config"))
        self.buttons.append(ConfigButtons(self.screen, 350, 500, 220, 50, "Start with Custom Settings", 20, (0, 255, 0), (128, 128, 128), self.start_game, "config", None))
        self.buttons.append(ConfigButtons(self.screen, 50, 500, 220, 50, "Back to Main Menu", 20, (0, 255, 0), (128, 128, 128), self.change_page, "config", "menu"))
        self.buttons.append(ConfigButtons(self.screen, 50, 500, 220, 50, "Back to Main Menu", 20, (0, 255, 0), (128, 128, 128), self.change_page, "controls", "menu"))
        self.buttons.append(ConfigButtons(self.screen, 350, 500, 220, 50, "Controls", 20, (0, 255, 0), (128, 128, 128), self.change_page, "menu", "controls"))

        self.toggles = []
        self.toggles.append(ConfigToggles(self.screen, 40, 5, 25, 25, Configs.Configs, 'loadGrass', "Load a brand new map upon start"))
        self.toggles.append(ConfigToggles(self.screen, 40, 35, 25, 25, Configs.Configs, 'autoDiscover', "Start with full map discovered"))
        self.toggles.append(ConfigToggles(self.screen, 40, 65, 25, 25, Configs.Configs, 'screen_size_Type', "Auto size the screen based on square count"))
        self.toggles.append(ConfigToggles(self.screen, 40, 95, 25, 25, Configs.Configs, 'seed', "Randomise the seed upon Start (Requires new map)"))

        self.valueBoxes = []
        self.valueBoxes.append(ConfigValueBox(self.screen, 40, 135, 50, 25, Configs.Configs, 'square_count', "The amount of Squares  the player can see"))
        self.valueBoxes.append(ConfigValueBox(self.screen, 40, 165, 50, 25, Configs.Configs, 'width', "The width of the screen"))
        self.valueBoxes.append(ConfigValueBox(self.screen, 40, 195, 50, 25, Configs.Configs, 'height', "The height of the screen"))
        self.valueBoxes.append(ConfigValueBox(self.screen, 40, 225, 50, 25, Configs.Configs, 'fps', "The frames per second the game runs at"))
        self.valueBoxes.append(ConfigValueBox(self.screen, 40, 255, 50, 25, Configs.Configs, 'sigma', "The sigma value for the perlin noise (requires new map)"))
        self.valueBoxes.append(ConfigValueBox(self.screen, 40, 285, 50, 25, Configs.Configs, 'green_constant', "The fixed green value added to the grass (requires new map)"))
        self.valueBoxes.append(ConfigValueBox(self.screen, 40, 315, 50, 25, Configs.Configs, 'seed', "The seed for the perlin noise (requires new map)"))

        self.controlText = []
        self.controlText.append(ControlsText(self.screen, 50, 50, 500, 500, "MOVEMENT - Arrow Keys", 24))
        self.controlText.append(ControlsText(self.screen, 50, 100, 500, 500, "MAP - m", 24))
        self.controlText.append(ControlsText(self.screen, 50, 150, 500, 500, "INVENTORY - i", 24))
        self.controlText.append(ControlsText(self.screen, 50, 200, 500, 500, "INTERACT - e", 24))
        self.controlText.append(ControlsText(self.screen, 50, 250, 500, 500, "CRAFTING - c", 24))
        self.controlText.append(ControlsText(self.screen, 50, 450, 500, 500, "Changed Keybinds will not display on this screen!", 24))

        for toggle in self.toggles:
            toggle.updateColour()

        self.warningText = ConfigToggles.font.render("WARNING: Changing these Configs may cause Crashes!", True, (255, 0, 0))

        self.run()

    @staticmethod
    def setStandardConfigs():

        # Standard Map Generation

        Configs.Configs.square_count = 5
        Configs.Configs.width = 800
        Configs.Configs.height = 800
        Configs.Configs.screen_size_Type = "Custom"
        Configs.Configs.fps = 60
        Configs.Configs.location_limits = {
            "P": 1,
            "S": 2,
            "E": 15,
            "C": 15,
            "T": 1,
            "M": 20
        }

        # Standard Map Generation

        Configs.Configs.loadGrass = True
        Configs.Configs.autoDiscover = False
        Configs.Configs.sigma = 10
        Configs.Configs.green_multiplier = 1.1
        Configs.Configs.seed = 7440  # Seed is randomised each time if Standard
        Configs.Configs.perlin_noise_octaves = 20

    def start_game(self):

        if self.page == "menu":
            Configs.Configs.config_Type = "Standard"
        else:
            Configs.Configs.config_Type = "Custom"
        Configs.Configs.play = True

        #self.fadeToBlack()
        self.running = False

    def start_noMap(self):
        Configs.Configs.loadGrass = False
        Configs.Configs.play = True
        self.start_game()

    def change_page(self, targetPage):

        self.timeSinceChange = time.time()

        if targetPage == "menu":
            self.setStandardConfigs()
            for toggle in self.toggles:
                toggle.updateColour()
            pygame.display.set_caption("Box Game Configuration and Setup - Main Screen")
            self.page = "menu"

        elif targetPage == "config":
            pygame.display.set_caption("Box Game Configuration and Setup - Custom Config Editor")
            self.page = "config"

        elif targetPage == "controls":
            pygame.display.set_caption("Box Game Configuration and Setup - Controls")
            self.page = "controls"

    def run(self):

        try:

            while self.running:

                self.clock.tick(self.fps)

                self.screen.fill((255, 255, 255))

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:

                        self.running = False
                        Configs.Configs.play = False

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        if time.time() - self.timeSinceChange > 0.1:

                            self.timeSinceChange = time.time()

                            for button in self.buttons:

                                if button.page == self.page:

                                    if button.click():
                                        break

                            for toggle in self.toggles:

                                if toggle.page == self.page:

                                    toggle.click()

                            for box in self.valueBoxes:

                                box.click("click")

                    if event.type == pygame.KEYDOWN:

                        for box in self.valueBoxes:
                            if box.awaitingInput:
                                box.inputText(self.convertKeyValueToChar(event.key))

                if self.running:

                    if self.page == "menu":
                        self.screen.blit(self.title, (0, 0))

                    elif self.page == "config":

                        self.screen.fill((255, 255, 255))
                        self.screen.blit(self.warningText, (50, 550))

                    elif self.page == "controls":
                        self.screen.fill((255, 255, 255))
                        for text in self.controlText:
                            text.draw()

                    for button in self.buttons:

                        if button.page == self.page:
                            if button.rect.collidepoint(pygame.mouse.get_pos()):
                                button.colour = button.hover_colour
                            else:
                                button.colour = (255, 255, 255)
                            button.draw()

                    for toggle in self.toggles:
                        if toggle.page == self.page:
                            toggle.draw()

                    for box in self.valueBoxes:
                        if box.page == self.page:
                            box.draw()

                pygame.display.flip()

            pygame.quit()

        except (pygame.error, KeyboardInterrupt, SystemExit):
            Configs.Configs.play = False
            pygame.quit()
            sys.exit()

    def fadeToBlack(self):

        # Create a black box over the entire screen, starts with full transparency
        # Should end at None transparency, over 2 seconds.

        blackBox = pygame.Surface((600, 600))
        blackBox.set_alpha(0)
        blackBox.fill((0, 0, 0))

        for i in range(0, 65):
            blackBox.set_alpha(i)
            self.screen.blit(blackBox, (0, 0))
            pygame.display.flip()
            self.clock.tick(30)
        self.screen.fill((0, 0, 0))

    #  This method below is the worst thing I have ever seen. DO NOT do this. Please.
    #  It pains me just to look at it. I am sorry for this.
    #  It is currently around 4 AM, and I am tired. I am sorry.

    @staticmethod
    def convertKeyValueToChar(value):
        if value == pygame.K_1:
            return 1
        elif value == pygame.K_2:
            return 2
        elif value == pygame.K_3:
            return 3
        elif value == pygame.K_4:
            return 4
        elif value == pygame.K_5:
            return 5
        elif value == pygame.K_6:
            return 6
        elif value == pygame.K_7:
            return 7
        elif value == pygame.K_8:
            return 8
        elif value == pygame.K_9:
            return 9
        elif value == pygame.K_0:
            return 0
        elif value == pygame.K_a:
            return "a"
        elif value == pygame.K_b:
            return "b"
        elif value == pygame.K_c:
            return "c"
        elif value == pygame.K_d:
            return "d"
        elif value == pygame.K_e:
            return "e"
        elif value == pygame.K_f:
            return "f"
        elif value == pygame.K_g:
            return "g"
        elif value == pygame.K_h:
            return "h"
        elif value == pygame.K_i:
            return "i"
        elif value == pygame.K_j:
            return "j"
        elif value == pygame.K_k:
            return "k"
        elif value == pygame.K_l:
            return "l"
        elif value == pygame.K_m:
            return "m"
        elif value == pygame.K_n:
            return "n"
        elif value == pygame.K_o:
            return "o"
        elif value == pygame.K_p:
            return "p"
        elif value == pygame.K_q:
            return "q"
        elif value == pygame.K_r:
            return "r"
        elif value == pygame.K_s:
            return "s"
        elif value == pygame.K_t:
            return "t"
        elif value == pygame.K_u:
            return "u"
        elif value == pygame.K_v:
            return "v"
        elif value == pygame.K_w:
            return "w"
        elif value == pygame.K_x:
            return "x"
        elif value == pygame.K_y:
            return "y"
        elif value == pygame.K_z:
            return "z"
        elif value == pygame.K_BACKSPACE:
            return "BACKSPACE"
        else:
            return None
