from helper.structs import Point
from enum import Enum


class Tile:
    def __init__(self, tile_content, x, y):
        self.TileContent = tile_content
        self.Position = Point(x, y)
        pass
    
    def __repr__(self):
        return "(%d, %d, %s)" % (self.Position.x, self.Position.y, TileContent.getName(self.TileContent))


class ResourceTile(Tile):
    def __init__(self, tile_content, x, y, amount_left, density):
        Tile.__init__(self, tile_content, x, y)
        self.AmountLeft = amount_left
        self.Density = density


class TileContent(Enum):
    Empty = 0
    Wall = 1
    House = 2
    Lava = 3
    Resource = 4
    Shop = 5
    Player = 6

    @staticmethod
    def getName(value):
        names = {
            TileContent.Empty: "Empty",
            TileContent.Wall: "Wall",
            TileContent.House: "House",
            TileContent.Lava: "Lava",
            TileContent.Resource: "Resource",
            TileContent.Shop: "Shop",
            TileContent.Player: "Player"
        }
        
        return names[value]
