from helper import Point, TileContent
from astar import AStarSolver

class Pathfinding(AStarSolver):
    def __init__(self):
        AStarSolver.__init__(self, Point)
        self.map = None
    
    def setMap(self, map):
        self.map = map
    
    def is_valid_neighbor(self, node):
        return self.map.tiles[node.x][node.y].TileContent == TileContent.Empty