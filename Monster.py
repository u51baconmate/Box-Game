import json
import pygame


class Monster:

    monsters = []

    def __init__(self, name, health, weapon, drops, abilities, skills, resistances, sprite):

        self.name = name
        self.health = health
        self.weapon = weapon
        self.drops = drops
        self.abilities = abilities
        self.skills = skills
        self.resistances = resistances
        self.sprite = sprite


def loadMonsters():
    with open("Monsters.json", "r") as file:
        data = json.load(file)

    for monster in data:
        Monster(monster["name"], monster["health"], monster["weapon"], monster["drops"], monster["abilities"], monster["skills"], monster["resistances"], monster["sprite"])

    for monster in Monster.monsters:

        if monster.sprite:

            try:
                monster.sprite = pygame.image.load(f"Tile_Images/{monster.sprite}")

            except (ModuleNotFoundError, FileNotFoundError):
                print(f"Failed to load sprite for {monster.name}")
                monster.sprite = pygame.image.load("Tile_Images/null.png")
