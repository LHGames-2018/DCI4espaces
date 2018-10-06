# Insert here all custom implementation for the bot.
from helper import *

def distance(a, b):
    return abs(b.x - a.x) + abs(b.y - a.y)

def distanceTo(target):
    return lambda tile: distance(tile.Position, target)

def sort_by_distance(tile_list, current_point):
    return sorted(tile_list, key=distanceTo(current_point))

def get_closest(tile_list, current_point):
    return sort_by_distance(tile_list, current_point)[0]