import csv
import random
from Configs.Configs import Configs
import Monster

class Tile:

    tiles = []
    tile_count = 0

    def __init__(self, x, y, display_char, player_present, seen, discovered, completed):
        """
        :param x: x position of the tile
        :param y: y position of the tile
        :param display_char: character displayed on the tile (P, E, S, C, T, M, F)
        :param player_present: determines if the player is on the tile currently
        :param seen: determines if the tile has been seen by the player at any point
        """

        self.x = x
        self.y = y
        self.display_char = display_char

        if self.display_char == "M":
            self.monster = ...

        self.player_present = player_present
        self.grassTile = f"G{Tile.tile_count}" if display_char != "#" else f"G1"
        self.seen = seen
        self.discovered = discovered
        self.completed = completed

        Tile.tile_count += 1

        if Tile.tile_count % 1600 == 0:
            print("<tile> Created all Tiles!")


class Maps:

    def __init__(self):

        self.map = []
        self.vision = []
        self.limits = Configs.location_limits

        self.createMapObjects(Maps.loadDefaultMap("map"))
        self.assignCharToTile()

    @staticmethod
    def loadDefaultMap(returnVal):

        loadedMap = []

        with open(Configs.default_world_save_location, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                loadedMap.append(row)

        if returnVal == "size":  # If the returnVal is "size", return the size of the map
            return len(loadedMap)

        return loadedMap  # Otherwise, return the map

    def createMapObjects(self, loadedMap):

        for y in range(len(loadedMap)):

            row = []

            for x in range(len(loadedMap[y])):

                row.append(Tile(x, y, loadedMap[y][x], False, False if Configs.config_Type == "Standard" else Configs.autoDiscover, False, False))

            self.map.append(row)

    def assignCharToTile(self):

        for y in range(len(self.map)):

            for x in range(len(self.map[y])):

                for key in self.limits.keys():

                    while self.limits[key] > 0:

                        valid_x, valid_y = self.findAvailable()

                        if key == "P":
                            self.map[valid_y][valid_x].player_present = True
                            self.map[valid_y][valid_x].display_char = ' '
                            self.limits[key] -= 1
                            continue

                        self.map[valid_y][valid_x].display_char = key

                        self.limits[key] -= 1

    def findAvailable(self):
        while True:
            x, y = self.randomMapPosition(len(self.map))
            if self.checkAvailable(x, y):
                return x, y

    def checkAvailable(self, x, y):
        return self.map[y][x].display_char == " "  # Should return True if the x,y position is an empty space

    @staticmethod
    def randomMapPosition(map_size):
        return random.randint(1, map_size - 1), random.randint(1, map_size - 1)

    def displayMap(self):
        print("<map> Displaying Map!")
        for row in self.map:
            for tile in row:

                if tile.player_present:
                    print("P", end=' ')
                    continue

                print(tile.display_char, end=' ')
            print()

    def playerPosition(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x].player_present:
                    return x, y
        return None

    def movePlayer(self, direction):

        direction = direction.upper()

        player_x, player_y = self.playerPosition()

        previous_x, previous_y = player_x, player_y

        match direction:

            case "W":
                player_y = player_y - 1 if self.map[player_y - 1][player_x].display_char != "#" else player_y

            case "A":
                player_x = player_x - 1 if self.map[player_y][player_x - 1].display_char != "#" else player_x

            case "S":
                player_y = player_y + 1 if self.map[player_y + 1][player_x].display_char != "#" else player_y

            case "D":
                player_x = player_x + 1 if self.map[player_y][player_x + 1].display_char != "#" else player_x

            case _:
                print("Invalid Direction!")
                return

        if player_x != previous_x or player_y != previous_y:  # If the player has moved, update player position
            self.map[previous_y][previous_x].player_present = False
            self.map[player_y][player_x].player_present = True
            # if the player has entered a special tile, print that tile

    @staticmethod
    def getBounds():

        SC = Configs.square_count

        lower_bound = (SC // -2) + 1

        upper_bound = lower_bound + SC

        return lower_bound, upper_bound

    def playerVision(self):

        x, y = self.playerPosition()

        self.vision = []

        lower_bound, upper_bound = Maps.getBounds()

        for i in range(lower_bound, upper_bound):

            row = []

            for j in range(lower_bound, upper_bound):

                if 0 <= x+j < len(self.map) and 0 <= y+i < len(self.map):
                    new_x, new_y = x+j, y+i

                    row.append(self.map[new_y][new_x])
                    self.map[new_y][new_x].seen = True

                else:
                    row.append(self.map[0][0])

            self.vision.append(row)

    def returnTileType(self):
        player_x, player_y = self.playerPosition()
        return self.map[player_y][player_x].display_char

    def returnTile(self, x, y):
        return self.map[y][x]

    def completeTile(self):
        player_x, player_y = self.playerPosition()
        self.map[player_y][player_x].completed = True
        self.map[player_y][player_x].display_char = " "






