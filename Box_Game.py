
import random
import time

from Items.LoadAll import loadAllItems
from World.Map import Maps
from World.Map import testWorld


#  Intended for one player and one player only.


class Box:

    boxes = []

    def __init__(self, name, contents, price):
        self.name = name
        self.contents = contents
        self.price = price
        Box.boxes.append(self)

    def openBox(self, cash):

        if not self.canAfford(cash):
            return "Can't Afford"

        if self.boxEmpty():
            return "Box is empty!"

        return self.reward()

    def canAfford(self, cash):
        return cash >= self.price

    def boxEmpty(self):
        return not self.contents  # Should return True if empty

    def reward(self):
        position = self.randomItem()

        return self.contents[position]

    def randomItem(self):
        return random.randint(0, len(self.contents) - 1)

    @classmethod
    def boxNames(cls):
        names = [box.name for box in Box.boxes]
        return names

    @staticmethod
    def printBoxNames(names):
        print('| ' + ' \t '.join(names) + ' |')




class Shop:

    def __init__(self, shopItems: list, startItemsCount):     
        self.shopItems = shopItems
        #  self.createStartItems(startItemsCount)

    def addItem(self, item):

        if self.itemInShop(item):
            item.stock += 1
            return "Stock of the item has increased!"
        
        self.shopItems.append(item)
        return "Item added to the shop!"

    def itemInShop(self, item):
        return True if item in self.shopItems else False


class BoxShop:

    def __init__(self, boxes):
        self.boxes = boxes



class Game:

    def __init__(self, playerName: str, initialShopItems: list) -> None:
        # self.player = Player(playerName)
        self.shop = Shop(initialShopItems, 3)
        print(self.shop.shopItems)
        self.GameLoop()


# Main Code

# Create a round class 
# Create a shop for the round
# Create Items for the round
# Create a player for the round
# Create 


if __name__ == "__main__":
    print("Start the program!")
    input("Chat are we ready? ")
    #  Game("Tomas", ["Metal", "Iron", "DeepWoken", "Rogue Lineage"])
    # loadAllItems(True)
    testWorld()

input("Name is not equal to __main__.")
