from helper.tile import TileContent
from helper import Point
from helper.aiHelper import *

class PathingActions:

    # Move the player towards a direction. If a "triggeringTileContent" is encountered,
    # change the action of the player from moving to "action".
    # "direction" must be a unit vector, ex: Point(-1, 0) for left.
    @staticmethod
    def doActionInPath(gameMap, currentPosition, direction, triggeringTileContent, action):

        # To cut down a tree, you must be on the tree instead of beside. 
        nextPosition = Point(currentPosition.x + direction.x, currentPosition.y + direction.y)

        # If there is a wall at the given position, destroy it.
        if gameMap.getTileAt(nextPosition) == triggeringTileContent:
            return action(direction)
        else:
            return create_move_action(direction)



    