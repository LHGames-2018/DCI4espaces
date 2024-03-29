from helper import Point, TileContent
from bot.astar import AStarSolver

class Pathfinding(AStarSolver):
    def __init__(self):
        AStarSolver.__init__(self, Point)
        self.map = None
    
    def setMap(self, map):
        self.map = map
    
    def is_valid_neighbor(self, node):
        try:
            return self.map.get(node.x, node.y).TileContent in [TileContent.Empty, TileContent.House]
        except IndexError:
            return False