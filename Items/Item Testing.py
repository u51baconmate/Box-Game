import json

with open('Materials/Materials.json', 'r') as jsonFile:
    data = json.load(jsonFile)


'''    for i in data[key]:
        BaseItem.createItem(i)'''


inventory = {
    "Iron Ingot": ["m1", "m2","m3", "m2"],
    "Oak Wood": ["ba", "da"],
    "Golden Armour": ["ad", "daw"],
    "Jack": ["ad", "daw"]
}


Sword_recipe = {
    "Blade": "Iron Ingot",
    "Hilt": "Leather"
}
Shield_recipe = {
    "Oak Wood": 2,
    "Iron Ingot": 5,
    "Temporary Item": 2,
    "Golden Armour": 2,
    "Jack": 3
}

for key, att in Shield_recipe.items():
    if key in inventory:
        if len(inventory[key]) >= att:
            print(f"The Inventory has {len(inventory[key])} {key}, The Recipe needs {att} {key}")
        else:
            print(f"The Inventory is missing {att-len(inventory[key])} more {key}")
    else:
        print(f"The Inventory is missing {att} {key}")


'''
crafting checks if the inventory meets the recipe and the counter of items

'''
