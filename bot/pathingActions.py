from helper.tile import TileContent
from helper import Point
from helper.aiHelper import *

class PathingActions:

    # Move the player towards a point. If a "triggeringTileContent" is encountered,
    # change the action of the player from moving to "action".
    # "point" must be a unit vector, ex: Point(-1, 0) for left.
    @staticmethod
    def doActionInPath(gameMap, playerInfo, point, triggeringTileContent, action):
        nextPosition = Point(playerInfo.x + point.x, playerInfo.y + point.y)
        # If there is a wall at the given position, destroy it.
        if gameMap.getTileAt(nextPosition) == triggeringTileContent:
            return action(point)
        else:
            return create_move_action(point)



    