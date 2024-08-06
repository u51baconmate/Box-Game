import Player.Inventory.Inventory as Inventory

class Player:

    def __init__(self):

        #self.username = username
        self.balance = 0

        self.inventory = Inventory.Inventory()

        self.spells = {
            "Slot One": None,
            "Slot Two": None,
            "Slot Three": None
        }

        self.abilities = {
            "Slot One": None,
            "Slot Two": None,
            "Slot Three": None
        }

        self.maxHP = 100
        self.HP = self.maxHP

        self.maxStamina = 100
        self.stamina = self.maxStamina
        self.staminaRecovery = 10

        self.maxMana = 100
        self.mana = 100
        self.manaRecovery = 0

        self.dodgeChance = 5
        self.dodged = False  # Completely avoid damage this turn.

        self.turn = False  # Include method for self.endTurn(), which is run after an ability and spell is used, or the player decides to end their turn

        self.level = 1
        self.experience = 0

        # Equipment, which is a dictionary of the player's equipment
        # Where each key is the type of equipment, and the value is the object of the equipment itself

        self.equipment = {
            "weapon": None,
            "helmet": None,
            "boots": None,
            "legs": None,
            "chest": None,
            "accessory": None,
            "accessory2": None
        }

        # Effects, which is a dictionary of the player's effects
        # Where each key is the type of effect, and the value is the duration of the effect (in turns)

        self.effects = {
            "bleed": 0,
            "fire": 0,
            "poison": 0,
            "stun": 0,
            "silence": 0,
            "confusion": 0,
            "frozen": 0,
            "suffocating": 0,
            "regeneration": 0,
            "defence": 0,
            "light-footed": 0
        }

        #  Resistances, which is a dictionary of the player's resistances
        #  Where each key is the type of resistance, and the value is the resistance value (as a multiplier) (e.g. 0.5 for 50% resistance) and (e.g. 1.5 for 150% damage taken)

        self.resistances = {
            "bleed": 0,
            "fire": 0,
            "poison": 0,
            "stun": 0,
            "silence": 0,
            "confusion": 0,
            "frozen": 0,
            "suffocating": 0,
            "physical": 0,
            "magical": 0
        }

    def equipEquipment(self, item, target):
        print("running equipEquipment")
        """
        :param equipment: the equipment to be equipped
        :param target: the target to equip the equipment to
        :return: None
        """

        if target in self.equipment.keys():
            self.equipment[target] = item

        if target != "weapon" and item:
            self.calculateEquipmentStats(item, True)

    def unequipEquipment(self, target):
        """
        :param target: the target to unequip the equipment from
        :return: None
        """
        item = self.equipment[target]

        if target in self.equipment.keys():
            self.equipment[target] = None

        if target != "weapon" and item:
            self.calculateEquipmentStats(item, False)

    def calculateEquipmentStats(self, item, add=True):  # Temporary function to print the equipment, remove later TODO: remove
        """
        :param item: The Item Object that was equipped or de-equipped
        :param add: True if the item was equipped, False if the item was unequipped
        :return: None, probably
        """

        if add:
            self.maxHP += item.healthBonus
            self.HP += item.healthBonus
            self.maxMana += item.manaBonus
            self.mana += item.manaBonus
            self.maxStamina += item.staminaBonus
            self.stamina += item.staminaBonus
            self.staminaRecovery += item.staminaRecoveryBonus
            self.manaRecovery += item.manaRecoveryBonus
            self.dodgeChance += item.dodgeChanceBonus

            for key in item.armourResistancesBonus:
                self.resistances[key] += item.armourResistancesBonus[key] if key in item.armourResistancesBonus.keys() else 0

        else:
            self.maxHP -= item.healthBonus
            self.HP -= item.healthBonus
            self.maxMana -= item.manaBonus
            self.mana -= item.manaBonus
            self.maxStamina -= item.staminaBonus
            self.stamina -= item.staminaBonus
            self.staminaRecovery -= item.staminaRecoveryBonus
            self.manaRecovery -= item.manaRecoveryBonus
            self.dodgeChance -= item.dodgeChanceBonus

            for key in item.armourResistancesBonus:
                self.resistances[key] -= item.armourResistancesBonus[key] if key in item.armourResistancesBonus.keys() else 0

    def statsCap(self, onFrame=True):
        """
        :return: None
        """
        if onFrame:
            if self.HP > self.maxHP:
                self.HP -= 1

            if self.stamina > self.maxStamina:
                self.stamina -= 1

            if self.mana > self.maxMana:
                self.mana -= 1
        else:
            if self.HP > self.maxHP:
                self.HP = self.maxHP

            if self.stamina > self.maxStamina:
                self.stamina = self.maxStamina

            if self.mana > self.maxMana:
                self.mana = self.maxMana


    # TODO:

    # add a function that checks what effects are on the player
    # add a function to calculate the damage each does
    # add a function to apply the damage to the player
    # add a function to modify these effects and their durations
    # add a function to remove these effects when their duration is over
    # ensure to include calculations for resistances.
