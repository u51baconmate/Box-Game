import Items.BaseItem as BaseItem
import pygame


class Inventory:

    def __init__(self):

        # this is a dict, where key,value = item_id, amount
        self.contents = {}

        # probably not needed
        self.raw_contents = []

        self.weight_limit = 50

        self.current_weight = 0

        self.highest_weight_reached = 0

    def add_item(self, item, amount=1):
        """
        :param item: The Item Object to be added
        :param amount: The amount of this object to be added
        :return: No Return
        """

        self.raw_contents.append(item)

        if item.item_id in self.contents:
            self.contents[item.item_id] += amount

        else:
            self.contents[item.item_id] = amount

        self.current_weight += item.weight * amount

        if self.current_weight > self.highest_weight_reached:
            self.highest_weight_reached = self.current_weight

    def remove_item(self, item, amount=1):
        """
        :param item: The Item Object to be removed
        :param amount: The amount of this object to be removed
        :return: No Return
        """

        if item.item_id in self.contents:

            self.raw_contents.remove(item)

            self.contents[item.item_id] -= amount
            self.current_weight -= item.weight * amount

            if self.contents[item.item_id] <= 0:
                del self.contents[item.item_id]

        else:
            print("<inventory> Item not found in inventory")
            return

    def output_inventory(self):
        for item_id, amount in self.contents.items():
            print(f"{item_id} ({BaseItem.Item.returnItemFromID(item_id).name}) : {amount}")


