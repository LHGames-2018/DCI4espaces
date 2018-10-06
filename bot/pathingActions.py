from helper.tile import TileContent
from helper import Point
from helper.aiHelper import *

class PathingActions:

    @staticmethod
    def destroyInPath(gameMap, playerInfo, move):
        nextPosition = Point(playerInfo.x + move.x, playerInfo.y + move.y)
        # If there is a wall at the given position, destroy it.
        if gameMap.getTileAt(nextPosition) == TileContent.Wall:
            return create_attack_action(move)
        else:
            return create_move_action(move)