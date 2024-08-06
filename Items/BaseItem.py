class Item:

    items = []
    materials = []
    armours = []
    weapons = []
    accessories = []

    #  Contains ALL items in the game, inc materials, weapons and armours, which each have their own stats.
    # These other items will have their own separate subclass for themselves.

    def __init__(self, item_id, name, description, base_value, rarity, weight, item_type, recipe, craft_amount, carry_limit, sprite=None):
        """
        :param item_id: the id of the item
        :param name: the name of the item
        :param description: the description shown in inventory
        :param base_value: the value of the item it starts with, influences the value of the item
        :param rarity: determines drop rate, and item background colour (e.g. white, green, blue, purple, orange)
        :param weight: the weight of the item in the inventory
        :param item_type: the type of item it is, e.g. material, weapon, armour, accessory
        :param recipe: the recipe for the item, if it is craftable, stored as a dictionary
        :param craft_amount: the amount of items that are crafted from the recipe
        :param carry_limit: the limit of how many of the item can be carried in the inventory
        :param sprite: the sprite (image) of the item, if it has one
        """

        self.item_id = item_id
        self.name = name
        self.description = description
        self.baseValue = base_value
        self.value = self.baseValue
        self.rarity = rarity
        self.weight = weight
        self.itemType = item_type
        self.recipe = recipe
        self.craftAmount = craft_amount
        self.carryLimit = carry_limit
        self.sprite = sprite

    @staticmethod
    def returnItemFromID(item_id):

        for item in Item.items:

            if item.item_id == item_id:

                return item



