import json
import pygame
import random  # get rid of this later

import Items.BaseItem as BaseItem
import Items.Materials.Materials as Materials
import Items.Armours.Armours as Armours
import Items.Weapons.Weapons as Weapons



# Import Materials from Materials.json

def loadMaterials():
    with open("Items/Materials/Materials.json", "r") as file:
        data = json.load(file)

    for material in data:
        Materials.Material(material["id"], material["name"], material["description"], material["base_value"], material["rarity"], material["weight"], material["item_type"], material["recipe"], material["craft_amount"], material["carry_limit"], material["sprite"], material["material_name"])

    for material in Materials.Material.materials:
        if material.sprite:
            try:
                material.sprite = pygame.image.load(f"Items/Item_Icons/{material.sprite}")
            except (ModuleNotFoundError, FileNotFoundError):
                print(f"Failed to load sprite for {material.name}")
                material.sprite = pygame.image.load("Items/Item_Icons/missing.png")


def loadArmours():
    with open("Items/Armours/Armours.json", "r") as file:
        data = json.load(file)

    for armour in data:
        Armours.Armour(armour["item_id"], armour["name"], armour["description"], armour["base_value"], armour["rarity"], armour["weight"], armour["item_type"], armour['armour_type'], armour["recipe"], armour["craft_amount"], armour["carry_limit"], armour["sprite"], armour["health_bonus"], armour["mana_bonus"], armour["stamina_bonus"], armour["staminaRecoveryBonus"] ,armour["manaRecoveryBonus"], armour["dodgeChanceBonus"], armour["armourResistancesBonus"])

    for armour in Armours.Armour.armours:
        if armour.sprite:
            try:
                armour.sprite = pygame.image.load(f"Items/Item_Icons/{armour.sprite}")
            except (ModuleNotFoundError, FileNotFoundError):
                print(f"Failed to load sprite for {armour.name}")
                armour.sprite = pygame.image.load("Items/Item_Icons/missing.png")


def loadWeapons():
    with open("Items/Weapons/Weapons.json", "r") as file:
        data = json.load(file)

    for weapon in data:
        Weapons.Weapon(weapon["item_id"], weapon["name"], weapon["description"], weapon["base_value"], weapon["rarity"], weapon["weight"], weapon["item_type"], weapon["weapon_type"], weapon["recipe"], weapon["craft_amount"], weapon["carry_limit"], weapon["sprite"], weapon["damage"], weapon["attack_speed"], weapon["critChance"], weapon["critDamage"], weapon["pen"], weapon["damage_type"], weapon["effects"], weapon["stamina_cost"])

    for weapon in Weapons.Weapon.weapons:
        if weapon.sprite:
            try:
                weapon.sprite = pygame.image.load(f"Items/Item_Icons/{weapon.sprite}")
            except (ModuleNotFoundError, FileNotFoundError):
                print(f"Failed to load sprite for {weapon.name}")
                weapon.sprite = pygame.image.load("Items/Item_Icons/missing.png")

# File will contain loading all items, loading player data, loading enemies, loading quests, loading locations, loading events, loading shops, loading crafting recipes
# loading all items will be done by loading all items from their respective json files
# REMEMBER: The order of loading is important, as some items may require other items to be loaded first


def returnItemDict():
    loadMaterials()
    loadArmours()
    loadWeapons()
    return {
            "Items": BaseItem.Item.items,
            "Materials": BaseItem.Item.materials,
            "Armours": BaseItem.Item.armours,
            "Weapons": BaseItem.Item.weapons
            }


def someFunnyTesting(game_object):
    pass
    #game_object.player.equipment['Helmet'] = BaseItem.Item.returnItemFromID("6009")
    #game_object.player.equipment['Boots'] = BaseItem.Item.returnItemFromID("6012")
    #game_object.player.equipment['Legs'] = BaseItem.Item.returnItemFromID("6011")
    #game_object.player.equipment['Chest'] = BaseItem.Item.returnItemFromID("6010")


def unequipAll(game_object):
    for key in game_object.player.equipment:
        game_object.player.equipment[key] = None
    game_object.player.weapon = None


def equipRandomArmour(game_object):
    options = ["Helmet", "Boots", "Legs", "Chest"]
    options = random.choice(options)
    if options == "Helmet":
        game_object.player.equipment['helmet'] = BaseItem.Item.returnItemFromID("6009")
    elif options == "Boots":
        game_object.player.equipment['boots'] = BaseItem.Item.returnItemFromID("6012")
    elif options == "Legs":
        game_object.player.equipment['legs'] = BaseItem.Item.returnItemFromID("6011")
    elif options == "Chest":
        game_object.player.equipment['chest'] = BaseItem.Item.returnItemFromID("6010")



