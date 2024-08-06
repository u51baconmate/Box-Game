import time

import pygame
import random
import sys

import Configs.Configs as Configs
import World.Map as Map
import Tile_Images.LoadImages as LoadImages
import GUIs.GUIs as GUIs
import Player.Player as Player
import Configs.Config_Screen as ConfigScreen
import Items.LoadAll as LoadItems
import GUIs.FightGUIs as FightGUIs



class Game:

    def __init__(self, Setup_Type):

        # type is either "Standard" or "Custom".
        # Standard will use predefined values for width and height.
        # Custom will allow the user to input their own values via the Configs file.

        pygame.init()

        # check if font module is already initialized
        if not pygame.font.get_init():
            pygame.font.init()

        if Setup_Type == "Standard":
            Configs.Configs.square_count = 5
            self.width = 800
            self.height = 800
            self.fps = 60

        elif Setup_Type == "Custom":
            self.width = Configs.Configs.width if Configs.Configs.screen_size_Type == "Custom" else Configs.autoSizeFinder(Configs.Configs.width, Configs.Configs.square_count)
            self.height = Configs.Configs.height if Configs.Configs.screen_size_Type == "Custom" else Configs.autoSizeFinder(Configs.Configs.height, Configs.Configs.square_count)
            self.fps = Configs.Configs.fps

        else:
            raise ValueError("Invalid Setup Type! Please use 'Standard' or 'Custom'.")

        load_image = pygame.image.load("loading_image.png")
        load_image = pygame.transform.scale(load_image, (self.width, self.height))
        pygame.display.set_caption("Loading...")

        self.font = pygame.font.Font(None, 24)

        self.items = LoadItems.returnItemDict()

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.blit(load_image, (0, 0))
        pygame.display.flip()
        self.running = True
        self.clock = pygame.time.Clock()

        self.player = Player.Player()

        print("Loading Maps, this might take a while...")

        self.images, self.grasses = LoadImages.loadImages(self.sizeOfSquare()[0], self.sizeOfSquare()[1], 40, 40)

        self.GUIs = GUIs.GUI(self.player, self.screen, self.images, self.font)

        self.fightGUI = FightGUIs.FightingGUI(self.player, self.screen, None, 0)

        self.world = Map.Maps()

        self.action = "traversing"  # the initial action is traversing

        self.frame = 0

    def sizeOfSquare(self):

        SC = Configs.Configs.square_count

        return self.width / SC, self.height / SC

    def drawArmour(self, player_pos):

        scale_size = self.sizeOfSquare()

        for key,value in self.player.equipment.items():
            if value:
                self.screen.blit(pygame.transform.scale(value.sprite, (scale_size[0], scale_size[1])), (player_pos[1] * self.sizeOfSquare()[0], player_pos[0] * self.sizeOfSquare()[1]))

    def draw_vision(self):

        square_width, square_height = self.sizeOfSquare()

        player_pos = None

        for row in range(len(self.world.vision)):

            for col in range(len(self.world.vision)):

                char = self.world.vision[row][col].display_char

                if self.world.vision[row][col].player_present:
                    player_pos = (row, col)
                    #  char = "P"

                self.screen.blit(self.grasses[self.world.vision[row][col].grassTile], (col * square_width, row * square_height))

                if char not in self.images.keys() and char != " ":
                    # the image does not exist (yet)
                    self.screen.blit(self.images["null"], (col * square_width, row * square_height))

                elif char != " ":
                    self.screen.blit(self.images[char], (col * square_width, row * square_height))

        if player_pos:
            self.screen.blit(self.images['P'], (player_pos[1] * square_width, player_pos[0] * square_height))

        self.drawArmour(player_pos)

    def draw_map(self):
        # draw the tiles that the player has seen, if they have not seen it then draw gray fog
        height, width = self.screen.get_height(), self.screen.get_width()
        height = height//len(self.world.map)
        width = width//len(self.world.map)
        square_width, square_height = height, width
        print(f"{square_width, square_height}")
        print(f"{len(self.world.map)}")

        self.screen.fill((0, 128, 0))

        for row in range(len(self.world.map)):

            for col in range(len(self.world.map[row])):

                if not self.world.map[row][col].seen:

                    self.screen.blit(pygame.transform.scale(self.images["fog"], (square_height,square_width)), (col * square_width, row * square_height))

                else:

                    char = self.world.map[row][col].display_char

                    if self.world.map[row][col].player_present:
                        char = "P2"

                    self.screen.blit(pygame.transform.scale(self.grasses[self.world.map[row][col].grassTile],(square_height, square_width)), (col * square_width, row * square_height)), (col * square_width, row * square_height)

                    if char != " ":

                        if char not in self.images.keys():
                            self.screen.blit(pygame.transform.scale(self.images["null"],(square_height,square_width)), (col * square_width, row * square_height))

                        else:
                            self.screen.blit(pygame.transform.scale(self.images[char],(square_height,square_width)), (col * square_width, row * square_height))

    def updateTraversal(self):

        #  In this method, we will update features in the game that should be updated every frame, e,g Health Bar Colour, position and size.

        # This probably won't be used.

        pass

    # < --- Main Game Loop --- >

    def run(self):

        pygame.display.set_caption("Trust me, this game is awesome!")

        self.world.playerVision()
        self.draw_vision()

        try:

            while self.running:

                self.clock.tick(self.fps)

                self.frame += 1

                self.player.statsCap()  # ensure that the player stats can never go above the cap

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        self.running = False

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_p:
                            print("FPS: ", self.clock.get_fps())

                    if self.action == "traversing":

                        if event.type == pygame.KEYDOWN:

                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                self.world.movePlayer("w")

                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                self.world.movePlayer("s")

                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                self.world.movePlayer("a")

                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                self.world.movePlayer("d")

                            if event.key == pygame.K_i:
                                self.action = "inventory"

                            elif event.key == pygame.K_m:

                                self.action = "map"
                                self.draw_map()
                                continue

                            elif event.key == pygame.K_h:
                                self.player.HP += 50
                            elif event.key == pygame.K_j:
                                self.player.HP -= 50

                            if self.world.returnTileType() == "M":
                                self.action = "fighting"

                                self.world.playerVision()
                                self.draw_vision()

                                self.fightGUI.initiateFight()
                                break

                            self.world.playerVision()

                            self.draw_vision()

                    elif self.action == "inventory":

                        if event.type == pygame.KEYDOWN:

                            if event.key == pygame.K_i:

                                self.GUIs.unselectInventorySlot()

                                self.action = "traversing"

                                self.player.statsCap(False)

                                self.draw_vision()

                            elif event.key == pygame.K_8:
                                self.player.inventory.remove_item(self.items["Items"][random.randint(0, len(self.items["Items"])-1)])
                            elif event.key == pygame.K_9:
                                # add an item that is not in the inventory to the inventory
                                for j in range(7):
                                    for i in range(len(self.items["Items"])):
                                        if self.items["Items"][i].item_id not in self.player.inventory.contents.keys():
                                            self.player.inventory.add_item(self.items["Items"][i])
                                            break
                            elif event.key == pygame.K_0:
                                # add 5 random items to the inventory
                                for j in range(5):
                                    random_item = self.items["Items"][random.randint(0, len(self.items["Items"])-1)]
                                    self.player.inventory.add_item(random_item)

                        elif event.type == pygame.MOUSEBUTTONDOWN:

                            self.GUIs.inventoryClick(event.pos)

                    elif self.action == "map":

                        if event.type == pygame.KEYDOWN:

                            if event.key == pygame.K_m:

                                self.action = "traversing"
                                self.draw_vision()
                                continue

                # these are frame updates

                if self.action == "traversing":

                    self.GUIs.drawUIs()

                elif self.action == "inventory":

                    self.screen.fill((61, 35, 9))

                    self.GUIs.drawInventory()

                elif self.action == "map":

                    pass

                elif self.action == "fighting":

                    if self.fightGUI.inAnim:
                        return

                    else:
                        self.world.completeTile()
                        self.action = "traversing"
                        self.draw_vision()

                pygame.display.flip()

        except KeyboardInterrupt:
            print("Game has been closed. 1")
            print("Exiting...")



if __name__ == '__main__':

    ConfigScreen.ConfigScreen()

    if not Configs.Configs.play:
        print("Exiting...")
        pygame.quit()
        sys.exit()

    del ConfigScreen.ConfigScreen

    game = Game(Configs.Configs.config_Type)
    print("Game has been created, configuration selected: ", Configs.Configs.config_Type)
    print(f"Width: {game.width}, Height: {game.height}, FPS: {game.fps}")
    print(f"The size of each square is: {game.sizeOfSquare()}")
    game.world.displayMap()
    LoadItems.someFunnyTesting(game)
    game.run()
    print("Game has been closed. 2")
    print("Exiting...")





pygame.quit()
sys.exit()







