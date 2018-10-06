from helper.structs import Point

class MapHelper:

    # Helper method to determine what is the next move in order to move
    # towards something. It uses manhattan movement in order to retrieve a point.
    # Ex: Point(-1, 0) to move left.
    @staticmethod
    def getMoveTowards(fromPoint, toPoint):
        distX = toPoint.x - fromPoint.x
        distY = toPoint.y - fromPoint.y

        absoluteDistX = abs(distX)
        absoluteDistY = abs(distY)
        
        # If we are closer in X position, move in the y axis
        if absoluteDistX <= absoluteDistY and distY != 0:
            return Point(0, distY // absoluteDistY) # abs is used to keep the sign on the move.
        elif absoluteDistX > absoluteDistY and distX != 0:
            return Point(distX // absoluteDistX, 0)
        else:
            print("[MapHelper.getMoveTowards] You are already at the given position.")
            return Point(0, 0)

    @staticmethod
    def isNextTo(first, second):
        return abs(first.x - second.x) + abs(first.y - second.y) == 1

    @staticmethod
    def isOn(first, second):
        return abs(first.x - second.x) + abs(first.y - second.y) == 0