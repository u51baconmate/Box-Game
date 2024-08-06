import pygame
import Items.BaseItem as BaseItem

# temporarily import random >> remove later
import random


class ItemDescription:

    text_box = None

    def __init__(self, itemName, itemDescription, itemRarity, itemValue, itemWeight, xpos, ypos, width, height):

        self.itemName = itemName
        self.itemDescription = itemDescription
        self.itemRarity = itemRarity
        self.itemValue = itemValue
        self.itemWeight = itemWeight

        self.x_pos = xpos
        self.y_pos = ypos
        self.width = width
        self.height = height

        itemType = None
        # if armour, display resistances and bonuses, weapon, effect and damage, accessory, effect and bonus

        ItemDescription.text_box = self

    @staticmethod
    def createInitialObject(xpos, ypos, width, height):

        ItemDescription(None, None, None, None, None, xpos, ypos, width, height)

    def updateObject(self, item):

        self.itemName = item.name
        self.itemDescription = item.description
        self.itemRarity = item.rarity
        self.itemValue = item.value
        self.itemWeight = item.weight

    def clearSlot(self):

        self.itemName = None
        self.itemDescription = None
        self.itemRarity = None
        self.itemValue = None
        self.itemWeight = None


class EquipmentSlot:

    equipment_slots = 1

    def __init__(self, x_pos, y_pos, width, height, equipment_type):  # accessory will have 2  slots, the rest will have 1

        self.x_pos = x_pos

        self.y_pos = y_pos

        self.width = width

        self.height = height

        self.equipment_type = equipment_type

        self.slotType = None

        match equipment_type:
            case "helmet":
                self.sprite = pygame.transform.scale(pygame.image.load("GUIs/icons/helmet_slot.png"), (self.width, self.height))
                self.slotType = "armour"
            case "chest":
                self.sprite = pygame.transform.scale(pygame.image.load("GUIs/icons/chestplate_slot.png"), (self.width, self.height))
                self.slotType = "armour"
            case "legs":
                self.sprite = pygame.transform.scale(pygame.image.load("GUIs/icons/leggings_slot.png"), (self.width, self.height))
                self.slotType = "armour"
            case "boots":
                self.sprite = pygame.transform.scale(pygame.image.load("GUIs/icons/boots_slot.png"), (self.width, self.height))
                self.slotType = "armour"
            case "weapon":
                self.sprite = pygame.transform.scale(pygame.image.load("GUIs/icons/weapon_slot.png"), (self.width, self.height))
                self.slotType = "weapon"
            case "accessory":
                self.sprite = pygame.transform.scale(pygame.image.load("GUIs/icons/accessory_slot.png"), (self.width, self.height))
                self.slotType = "accessory"
            case "accessory2":
                self.sprite = pygame.transform.scale(pygame.image.load("GUIs/icons/accessory_slot.png"), (self.width, self.height))
                self.slotType = "accessory"
            case _:
                self.sprite = pygame.transform.scale(pygame.image.load("GUIs/icons/misc_icon.png"), (self.width, self.height))

        self.equipment = None

        EquipmentSlot.equipment_slots += 1

    def draw(self, screen):

            pygame.draw.rect(screen, (0, 0, 0), (self.x_pos - 2, self.y_pos - 2, self.width + 4, self.height + 4))

            pygame.draw.rect(screen, (190, 140, 70), (self.x_pos, self.y_pos, self.width, self.height))

            if self.equipment:

                screen.blit(pygame.transform.scale(self.equipment.sprite, (self.width, self.height)), (self.x_pos, self.y_pos))

            else:
                screen.blit(self.sprite, (self.x_pos, self.y_pos))

    def clicked(self, mouse_pos, player):

        if not (self.x_pos < mouse_pos[0] < self.x_pos + self.width and self.y_pos < mouse_pos[1] < self.y_pos + self.height):
            return

        if self.equipment:  # if there is an item in the slot, un-equip it

            player.inventory.add_item(self.equipment)  # add the item to the player's inventory

            self.equipment = None  # remove the item from the slot

            player.unequipEquipment(self.equipment_type)  # unequip the item from the player

            return

        if not InventorySlot.selectedSlot:  # if there is no item to equip, return

            return

        if InventorySlot.selectedSlot.item.itemType != self.slotType:  # if the item selected is not the same type as the equipment slot

            return

        if self.slotType == "armour":  # if the item is an armour, check if the armour type matches the equipment slot

            if InventorySlot.selectedSlot.item.armourType != self.equipment_type:  # if the armour type does not match the equipment slot, return

                return

            self.equipment = InventorySlot.selectedSlot.item  # equip the item to the slot

            player.equipEquipment(InventorySlot.selectedSlot.item, self.equipment_type)  # equip the item to the player

            player.inventory.remove_item(InventorySlot.selectedSlot.item)  # remove the item from the player's inventory

            InventorySlot.unselect()

            return

        self.equipment = InventorySlot.selectedSlot.item  # equip the item to the slot

        player.inventory.remove_item(InventorySlot.selectedSlot.item)  # remove the item from the player's inventory

        player.equipEquipment(InventorySlot.selectedSlot.item, self.equipment_type)  # equip the item to the player

        InventorySlot.unselect()


class EquipmentPlayerImage:

    image = None

    # the purpose of this class is to draw an image of the player with all their equipment on,

    # including weapons, armours, and accessories. This should be slightly scaled towards the size of the container it is in

    def __init__(self, x_pos, y_pos, width, height):

        self.x_pos = x_pos

        self.y_pos = y_pos

        self.width = width

        self.height = height

        EquipmentPlayerImage.image = self

    def draw(self, screen, images, player):

        # create a small outline around the player image

        # this is not duplicate code because its in different areas
        pygame.draw.rect(screen, (0, 0, 0), (self.x_pos - 2, self.y_pos - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(screen, (190, 140, 70), (self.x_pos, self.y_pos, self.width, self.height))

        # find the center of the box

        centre_x = self.x_pos + (self.width // 2) - (images["P"].get_width() // 2)
        centre_y = self.y_pos + (self.height // 2) - (images["P"].get_height() // 2)

        # draw the player's image in the center of the box

        screen.blit(images["P"], (centre_x, centre_y))

        # draw the player's equipment on top of the player's image

        for key, value in player.equipment.items():

            if value is not None:

                if value.sprite is not None:

                    # scale the image to the images["P"]'s size

                    value.sprite = pygame.transform.scale(value.sprite, (images["P"].get_width(), images["P"].get_height()))

                    screen.blit(value.sprite, (centre_x, centre_y))


class InventoryButton:

    buttons = []

    colour = (150, 100, 30)

    def __init__(self, x_pos, y_pos, width, height):

        self.x_pos = x_pos

        self.y_pos = y_pos

        self.width = width

        self.height = height

        if len(InventoryButton.buttons) == 0:
            self.icon = pygame.transform.scale(pygame.image.load("GUIs/icons/material_icon.png"), (self.width, self.height))
            self.targetPage = "material"

        elif len(InventoryButton.buttons) == 1:
            self.icon = pygame.transform.scale(pygame.image.load("GUIs/icons/armour_icon.png"), (self.width, self.height))
            self.targetPage = "armour"

        elif len(InventoryButton.buttons) == 2:
            self.icon = pygame.transform.scale(pygame.image.load("GUIs/icons/weapon_icon.png"), (self.width, self.height))
            self.targetPage = "weapon"

        elif len(InventoryButton.buttons) == 3:
            self.icon = pygame.transform.scale(pygame.image.load("GUIs/icons/accessory_icon.png"), (self.width, self.height))
            self.targetPage = "accessory"

        elif len(InventoryButton.buttons) == 4:
            self.icon = pygame.transform.scale(pygame.image.load("GUIs/icons/trash_icon.png"), (self.width, self.height))
            self.targetPage = "trash"

        else:
            self.colour = InventoryButton.colour

            self.selectedCol = (150, 100, 30)

            self.icon = None

            self.targetPage = "material"

        InventoryButton.buttons.append(self)

    def draw(self, screen):

        if InventoryUI.selectedPage == self.targetPage:
            # draw a small border around the button to show that it is selected
            pygame.draw.rect(screen, (0, 0, 0), (self.x_pos - 2, self.y_pos - 2, self.width + 4, self.height + 4))

        if not self.icon:
            pygame.draw.rect(screen, self.colour, (self.x_pos, self.y_pos, self.width, self.height))
            return

        screen.blit(self.icon, (self.x_pos, self.y_pos))

    def clicked(self, mouse_pos, player):

        if self.x_pos < mouse_pos[0] < self.x_pos + self.width and self.y_pos < mouse_pos[1] < self.y_pos + self.height:

            if self.targetPage != "trash":

                InventoryUI.selectedPage = self.targetPage

                InventorySlot.unselect()

            else:

                # trash the item in the selected slot

                try:
                    if InventorySlot.selectedSlot.item:

                        player.inventory.remove_item(InventorySlot.selectedSlot.item)

                        InventorySlot.selectedSlot.item = None
                        InventorySlot.selectedSlot.selected = False
                        InventorySlot.selectedSlot = None
                except AttributeError:
                    #  This just means that there is no item in the selected slot
                    pass


class InventorySlot:

    slots = []

    colour = (190, 140, 70)

    selectedSlot = None

    def __init__(self, x_pos, y_pos, width, height, item=None):

        self.x_pos = x_pos

        self.y_pos = y_pos

        self.width = width

        self.height = height

        self.colour = InventorySlot.colour

        self.item = item

        self.position = len(InventorySlot.slots) + 1

        self.selected = False

        self.selectedCol = (150, 100, 30)

        # each slot stores data for each material page, weapon page, armour page, accessory page

        InventorySlot.slots.append(self)

    def draw(self, screen, player=None, font=None):

        colour = self.selectedCol if self.selected else self.colour
        pygame.draw.rect(screen, colour, (self.x_pos, self.y_pos, self.width, self.height))

        # Draw the item if it exists
        if self.item:

            if self.item.sprite:

                item_sprite = pygame.transform.scale(self.item.sprite, (self.width, self.height))
                screen.blit(item_sprite, (self.x_pos, self.y_pos))

            if player:
                # basically draw a small number in the corner representing the amount of the item in the inventory

                count = player.inventory.contents[self.item.item_id] if self.item.item_id in player.inventory.contents.keys() else 0

                if count > 1:
                    text = font.render(str(count), True, (0, 0, 0))
                    screen.blit(text, (self.x_pos + self.width - 10, self.y_pos + self.height - 20))

        #  draw the item's sprite in the slot

    def clicked(self, mouse_pos):

        if self.x_pos < mouse_pos[0] < self.x_pos + self.width and self.y_pos < mouse_pos[1] < self.y_pos + self.height:

            if InventorySlot.selectedSlot and InventorySlot.selectedSlot != self:

                InventorySlot.selectedSlot.selected = False

            if not self.selected:

                self.selected = True

                InventorySlot.selectedSlot = self

            else:
                self.selected = False
                InventorySlot.selectedSlot = None

    @classmethod
    def unselect(cls):

        # unselect the selected slot, if there is one

        if cls.selectedSlot:

            cls.selectedSlot.selected = False
            cls.selectedSlot = None


class InventoryUI:

    selectedPage = "material"

    def __init__(self, player, screen, images, font):

        self.player = player

        self.screen = screen

        self.images = images

        self.font = font

        #  the inventory consists of 4 main parts:
        # 1. The main inventory where the items are displayed (top right)
        # 2. The equipment slots where the player's equipment is displayed (top left)
        # 3. The player's stats, which are displayed in the bottom left
        # 4. The Description of the item selected, which is displayed in the bottom right

        main_bg = (172, 116, 52)
        slot_bg = (190, 140, 70)

        scr_width = screen.get_size()[0]
        scr_height = screen.get_size()[1]

        self.main_inventory = {
            "main_box": {
                "colour": main_bg,
                "x_pos": scr_width * 0.45,
                "y_pos": scr_height * 0.05,
                "width": scr_width * 0.5,
                "height": scr_height * 0.5
            },
            "slots": [],
            "buttons": [],
            "player": player
        }

        gap = scr_width * 0.01
        for i in range(5):
            for j in range(5):

                if i != 4:
                    self.main_inventory["slots"].append(
                        InventorySlot(self.main_inventory["main_box"]["x_pos"] + gap + j * (scr_width * 0.1),
                                      self.main_inventory["main_box"]["y_pos"] + gap + i * (scr_height * 0.1),
                                      scr_width * 0.1 - 2 * gap, scr_height * 0.1 - 2 * gap))
                #elif j != 4:
                else:
                    self.main_inventory["buttons"].append(
                        InventoryButton(self.main_inventory["main_box"]["x_pos"] + gap + j * (scr_width * 0.1),
                                      self.main_inventory["main_box"]["y_pos"] + gap + i * (scr_height * 0.1),
                                      scr_width * 0.1 - 2 * gap, scr_height * 0.1 - 2 * gap))

        self.equipment_slots = {
            "main_box": {
                "colour": main_bg,
                "x_pos": scr_width * 0.05,
                "y_pos": scr_height * 0.05,
                "width": scr_width * 0.35,
                "height": scr_height * 0.55
            },
            "player_image": EquipmentPlayerImage(scr_width * 0.1, scr_height * 0.1, scr_width * 0.15, scr_height * 0.35),
            "slots": []
        }

        # equipment slots should have 3 along the bottom and 4 from top to bottom

        slots = ["helmet", "chest", "legs", "boots", "weapon", "accessory", "accessory2"]

        for i in range(4):
            self.equipment_slots['slots'].append(EquipmentSlot(scr_width * 0.275, scr_height * 0.1 + i * (scr_height * 0.092), scr_width * 0.075, scr_height * 0.075, slots[0]))
            print(slots[i], slots[0])
            slots.pop(0)

        for i in range(3):
            self.equipment_slots['slots'].append(EquipmentSlot(scr_width * 0.1 + i * (scr_width * 0.0885), scr_height * 0.47, scr_width * 0.075, scr_height * 0.075, slots[0]))
            slots.pop(0)

        self.player_stats = {
            "main_box": {
                "colour": main_bg,
                "x_pos": scr_width * 0.05,
                "y_pos": scr_height * 0.65,
                "width": scr_width * 0.4,
                "height": scr_height * 0.3
            },
            "Title": {
                "Text": "Current Stats :",
                "x_pos": scr_width * 0.055,
                "y_pos": scr_height * 0.65
            }

        }

        self.item_description = {
            "main_box": {
                "colour": main_bg,
                "x_pos": scr_width * 0.5,
                "y_pos": scr_height * 0.6,
                "width": scr_width * 0.45,
                "height": scr_height * 0.35
            },
            "text box": ItemDescription.createInitialObject(scr_width * 0.51, scr_height * 0.61, scr_width * 0.44, scr_height * 0.33)
        }

    def draw(self):

        self.drawMainInventory()

        self.drawEquipmentTab()

        self.drawPlayerStats()

        self.drawItemDescription()

        # draw the player's equipment in the equipment slots

    def drawPlayerStats(self):

        pygame.draw.rect(self.screen, self.player_stats["main_box"]["colour"], (
            self.player_stats["main_box"]["x_pos"], self.player_stats["main_box"]["y_pos"],
            self.player_stats["main_box"]["width"], self.player_stats["main_box"]["height"]))

        title = self.font.render(self.player_stats["Title"]["Text"], True, (0, 0, 0))

        self.screen.blit(title, (self.player_stats["Title"]["x_pos"], self.player_stats["Title"]["y_pos"]))

        y_position = self.player_stats["Title"]["y_pos"] + 20

        stats = {
            "HP": self.font.render(f"HP: {self.player.HP}/{self.player.maxHP}", True, (0, 0, 0)),
            "Mana": self.font.render(f"Mana: {self.player.mana}/{self.player.maxMana} | Recovery: {self.player.manaRecovery}", True, (0, 0, 0)),
            "Stamina": self.font.render(f"Stamina: {self.player.stamina}/{self.player.maxStamina} | Recovery: {self.player.staminaRecovery}", True, (0, 0, 0)),
            "Dodge": self.font.render(f"Dodge Chance: {self.player.dodgeChance}%", True, (0, 0, 0)),
            "Resistances": self.font.render(f"Resistances:", True, (0, 0, 0))
        }

        resistanceStats = {}
        for key, value in self.player.resistances.items():
            resistanceStats[key] = self.font.render(f"{key.capitalize()}: {value}", True, (0, 0, 0))

        for key, value in stats.items():

            self.screen.blit(value, (self.player_stats["Title"]["x_pos"], y_position))

            y_position += 25

        y_position -= 5

        count = 0

        for key, value in resistanceStats.items():

            if count % 2 == 0:
                self.screen.blit(value, (self.player_stats["Title"]["x_pos"], y_position))

            else:
                self.screen.blit(value, (self.player_stats["Title"]["x_pos"] + 100, y_position - 10))

            count += 1

            y_position += 10

    def drawItemDescription(self):

        # update item

        if InventorySlot.selectedSlot and InventorySlot.selectedSlot.item:
            ItemDescription.text_box.updateObject(InventorySlot.selectedSlot.item)
        else:
            ItemDescription.text_box.clearSlot()

        # for now just draw the text box size

        pygame.draw.rect(self.screen, self.item_description["main_box"]["colour"], (
            self.item_description["main_box"]["x_pos"], self.item_description["main_box"]["y_pos"],
            self.item_description["main_box"]["width"], self.item_description["main_box"]["height"]))

        if ItemDescription.text_box.itemName:
            name = self.font.render(f"Name: {ItemDescription.text_box.itemName}", True, (0, 0, 0))

            # if the description is longer than 30 characters, split it into two lines

            y_pos_print = self.item_description["main_box"]["y_pos"] + 10

            description2 = None

            if len(ItemDescription.text_box.itemDescription) > 30:

                split_index = ItemDescription.text_box.itemDescription.rfind(' ', 0, 30)
                if split_index == -1:
                    split_index = 30

                description = self.font.render(f"Description: {ItemDescription.text_box.itemDescription[:split_index]}", True, (0, 0, 0))
                description2 = self.font.render(f"{ItemDescription.text_box.itemDescription[split_index+1:]}", True, (0, 0, 0))

            else:
                description = self.font.render(f"Description: {ItemDescription.text_box.itemDescription}", True, (0, 0, 0))

            rarity = ItemDescription.text_box.itemRarity.capitalize()

            rarity = self.font.render(f"Rarity: {rarity}", True, (0, 0, 0))

            value = self.font.render(f"Value: {ItemDescription.text_box.itemValue}", True, (0, 0, 0))
            weight = self.font.render(f"Weight: {ItemDescription.text_box.itemWeight}", True, (0, 0, 0))

            self.screen.blit(name, (self.item_description["main_box"]["x_pos"] + 10, y_pos_print))

            y_pos_print += 30

            self.screen.blit(description, (self.item_description["main_box"]["x_pos"] + 10, y_pos_print))

            if description2:
                y_pos_print += 15
                self.screen.blit(description2, (self.item_description["main_box"]["x_pos"] + 10, y_pos_print))

            y_pos_print += 20
            self.screen.blit(rarity, (self.item_description["main_box"]["x_pos"] + 10, y_pos_print))
            y_pos_print += 20
            self.screen.blit(value, (self.item_description["main_box"]["x_pos"] + 10, y_pos_print))
            y_pos_print += 20
            self.screen.blit(weight, (self.item_description["main_box"]["x_pos"] + 10, y_pos_print))

            try:
                self.detailedDescription(InventorySlot.selectedSlot.item, y_pos_print + 20)
            except (AttributeError, TypeError) as Error:
                print("Encountered Error: Try-Except block at line 611 in inventoryUIs.py function : drawItemDescription")
                print(f"Error: {Error}")
                pass  # this just means that there is no item in the selected slot

    def detailedDescription(self, item, y_pos=100):

        # TODO: Finish Description once the items have been added and Logic implemented.

        match item.itemType:

            case "material":

                pass  # nothing to add

            case "armour":

                stats = {
                    "HP": self.font.render(f"HP: {item.healthBonus}", True, (0, 0, 0)),
                    "Mana": self.font.render(f"Mana: {item.manaBonus} | Recovery: {item.manaRecoveryBonus}", True, (0, 0, 0)),
                    "Stamina": self.font.render(f"Stamina: {item.staminaBonus} | Recovery: {item.staminaRecoveryBonus}", True, (0, 0, 0)),
                    "Dodge": self.font.render(f"Dodge Chance: {item.dodgeChanceBonus}%", True, (0, 0, 0)),
                    "Resistances": self.font.render(f"Resistances:", True, (0, 0, 0))
                }

                for key, value in stats.items():

                    self.screen.blit(value, (self.item_description["main_box"]["x_pos"] + 10, y_pos))

                    y_pos += 15

                    if key == "Dodge":
                        y_pos += 5

                resistanceStats = {
                    key: self.font.render(f"{key.capitalize()}: {value}", True, (0, 0, 0))
                    for key, value in item.armourResistancesBonus.items() if value != 0
                }

                count = 0
                y_pos += 5

                for key, value in resistanceStats.items():

                    if count % 2 == 0:
                        self.screen.blit(value, (self.item_description["main_box"]["x_pos"] + 10, y_pos))

                    else:
                        self.screen.blit(value, (self.item_description["main_box"]["x_pos"] + 120, y_pos))
                        y_pos += 15

                    count += 1

            case "weapon":

                stats = {
                    "Damage": self.font.render(f"Damage: {item.damage} | Type: {item.damageType.capitalize()}", True, (0, 0, 0)),
                    "Attack Speed": self.font.render(f"Attack Speed: {item.attackSpeed}", True, (0, 0, 0)),
                    "Crit Chance": self.font.render(f"Crit Chance: {item.critChance*100}% | Crit Multiplier: {item.critDamage}x", True, (0, 0, 0)),
                    "Penetration": self.font.render(f"Penetration: {item.armourPenetration}", True, (0, 0, 0)),
                    "Stamina Cost": self.font.render(f"Stamina Cost: {item.staminaCost}", True, (0, 0, 0)),
                    "Effects": self.font.render(f"Effects: ", True, (0, 0, 0))
                    }

                for key, value in stats.items():

                    self.screen.blit(value, (self.item_description["main_box"]["x_pos"] + 10, y_pos))

                    y_pos += 15

                    if key == "Stamina Cost":
                        y_pos += 5

            case "accessory":

                pass

            case _:
                print("No item type found")

    def drawEquipmentTab(self):

        pygame.draw.rect(self.screen, self.equipment_slots["main_box"]["colour"], (
            self.equipment_slots["main_box"]["x_pos"], self.equipment_slots["main_box"]["y_pos"],
            self.equipment_slots["main_box"]["width"], self.equipment_slots["main_box"]["height"]))

        self.equipment_slots["player_image"].draw(self.screen, self.images, self.player)

        for slot in self.equipment_slots["slots"]:
            slot.draw(self.screen)

    def drawMainInventory(self):

        # Draw the main inventory box

        pygame.draw.rect(self.screen, self.main_inventory["main_box"]["colour"], (self.main_inventory["main_box"]["x_pos"], self.main_inventory["main_box"]["y_pos"], self.main_inventory["main_box"]["width"], self.main_inventory["main_box"]["height"]))

        # Draw the slots in the main inventory

        if self.main_inventory["slots"]:
            for slot in self.main_inventory["slots"]:
                slot.draw(self.screen, self.player, self.font)

        # Draw the buttons in the main inventory

        if self.main_inventory["buttons"]:
            for button in self.main_inventory["buttons"]:
                button.draw(self.screen)

        self.assignItems(self.player)

    def assignItems(self, player):

        # clear the existing items in the slots

        for slot in self.main_inventory["slots"]:
            slot.item = None

        # for each item, check the next available slot in the inventory and assign it to that slot
        # it must match the page that the inventory is currently on

        assign_items = [item for item in [BaseItem.Item.returnItemFromID(item_id) for item_id in player.inventory.contents.keys()] if item.itemType == InventoryUI.selectedPage]

        i = 0

        for iteme in assign_items:

            self.main_inventory["slots"][i].item = iteme
            i += 1
