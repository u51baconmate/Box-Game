import sys
import os
import json


def findDefaultWorldSaveLocation():
    # find the file called "default_map.csv" in the "World" folder in the project directory

    try:

        for root, dirs, files in os.walk(os.getcwd()):  # Check main directory

            if "World" in dirs:  # Find the World directory

                for sub_root, sub_dirs, sub_files in os.walk(os.path.join(root, "World")):  # Check the World directory

                    if "default_map.csv" in sub_files:  # Check for the default_map.csv file

                        return os.path.join(sub_root, "default_map.csv")  # Return the path to the file

        raise FileNotFoundError("default_map.csv not found in the World directory.")
    except FileNotFoundError as e:
        print(e)
        input("Press Enter to exit...")
        sys.exit()


def autoSizeFinder(value, square_count):  # fun little function to find the closest value to the square count

    while value % square_count != 0:

        if value % square_count > square_count // 2:
            value += 1

        else:
            value -= 1

    return value


class Configs:

    """

    CHANGING THESE WILL HAVE NO EFFECT ON THE GAME, THESE ARE ONLY THE INITIAL CONFIGS

    THEY CAN BE CHANGED IN THE CONFIG START SCREEN IN THE GAME

    DO NOT CHANGE THESE UNLESS YOU KNOW WHAT YOU ARE DOING

    MOST SETTINGS *WILL* BE OVERWRITTEN BY THE CONFIG START SCREEN IN THE GAME

    """

    play = True  # DO NOT CHANGE

    # This is the default world save location, should automatically be set to the correct location
    default_world_save_location = findDefaultWorldSaveLocation()

    # This is the limits to each location, where P is the player, S is the shop, E is the encounter, C is the chest, T is the teleport and M is the monster
    location_limits = {
        "P": 1,
        "S": 2,
        "E": 15,
        "C": 15,
        "T": 1,
        "M": 20
    }  # ENTER THE AMOUNT OF EACH LOCATION YOU WANT IN THE GAME, WARNING: TOO MANY LOCATIONS MAY CAUSE ERRORS

    # ENTER CUSTOM PYGAME SETTINGS HERE

    width = 800  # ENTER WIDTH OF THE SCREEN

    height = 800  # ENTER HEIGHT OF THE SCREEN

    fps = 60  # ENTER FPS OF THE GAME

    square_count = 9  # ENTER THE AMOUNT OF SQUARES YOU WANT ON THE SCREEN (SET TO AUTO FOR AUTO-CONFIGURED SETTINGS) # Minimum value is 1

    screen_size_Type = "Custom"  # USE "Auto" FOR AUTO-CONFIGURED SETTINGS, USE "Custom" FOR CUSTOM SETTINGS.

    # TERRAIN GENERATION SETTINGS

    sigma = 8  # ENTER THE SIGMA VALUE FOR THE NOISE EFFECT

    green_multiplier = 1.1  # ENTER THE MULTIPLIER FOR THE GREEN VALUE OF THE GRASS

    green_constant = 10  # ENTER THE CONSTANT FOR THE GREEN VALUE OF THE GRASS

    perlin_noise_octaves = 20  # ENTER THE AMOUNT OF OCTAVES FOR THE PERLIN NOISE

    seed = 7440  # ENTER THE SEED FOR THE PERLIN NOISE

    loadGrass = True  # USE "True" TO CREATE A NEW MAP, USE "False" TO LOAD EXISTING MAP

    # CONFIG TYPE

    load_Data = "New"  # USE "New" FOR NEW GAME, USE "Load" FOR LOADING A GAME.
    # "Load" Currently not implemented.

    autoDiscover = True  # USE "True" TO START WITH THE WHOLE MAP DISCOVERED, USE "False" TO START WITH THE MAP UNDISCOVERED.

    config_Type = "Standard"  # USE "Standard" FOR DEFAULT SETTINGS, USE "Custom" FOR CUSTOM SETTINGS.


