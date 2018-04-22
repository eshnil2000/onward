import os
import glob
import pygame
from collections import namedtuple

dir_path = os.path.dirname(os.path.realpath(__file__))

Point = namedtuple('Point', 'x y')


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def get_files(a_dir):
    return glob.glob(os.path.join(a_dir, "*.png"))


def load_assets():
    # Loads all images in a folder and puts them in a dict with their file basenames as keys
    assets_dir = os.path.join(dir_path, "assets")
    categories = get_immediate_subdirectories(assets_dir)
    assets = {category: {os.path.splitext(os.path.basename(file))[0]: pygame.image.load(file).convert_alpha()
                         for file in get_files(os.path.join(assets_dir, category))} for category in categories}
    return assets


def load_data():
    # Loads all game-related data from text file and returns it in a dict
    return {}
