# Insert here all custom implementation for the bot.
from helper import *

def get_closest(tile_list, current_point):
    return sorted(tile_list, key=lambda tile: tile.Position.Distance(current_point))[0].Position


