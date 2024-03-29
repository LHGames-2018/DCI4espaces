from helper.tile import *
from helper.storageHelper import *
import pickle
import base64

persistent_map_key = "anus"

def save_persistent_map(persistent_map):
    encoded_map = base64.b64encode(pickle.dumps(persistent_map)).decode()
    StorageHelper.write(persistent_map_key, encoded_map)

def load_persistent_map():
    try:
        pickled_map = base64.b64decode(StorageHelper.read(persistent_map_key))
        return pickle.loads(pickled_map)
    except KeyError:
        return Persistent_map()

class Persistent_map:
    def __init__(self):
        self.width = 132
        self.height = 198
        self.tiles = []
        for col in range(self.width):
            self.tiles.append([])
            for row in range(self.height):
                self.tiles[col].append(Tile(TileContent.Unknown, col, row))

    def update(self, game_map, player_house):
        visible_map = game_map.tiles
        for row in visible_map:
            for tile in row:
                x = tile.Position.x
                y = tile.Position.y
                
                self.tiles[x][y] = tile
        
        x = player_house.x
        y = player_house.y
        self.tiles[x][y] = Tile(TileContent.House, x, y)
        self.tiles[x - 22][y] = Tile(TileContent.Shop, x, y)

        save_persistent_map(self)
    
    def findTileContent(self, content):
        for row in self.tiles:
            for col in row:
                if col.TileContent == content:
                    yield col

    def get(self, x, y):
        return self.tiles[x][y]
    
    def getTileAt(self, position):
        x = position.x
        y = position.y
        return self.tiles[x][y].TileContent

class GameMap:
    def __init__(self, serializedMap, xMin, yMin, wallsAreBreakable):
        self.xMin = xMin
        self.yMin = yMin
        self.wallsAreBreakable = wallsAreBreakable
        self.deserializeMap(serializedMap)
        self.initMapSize()

    def getTileAt(self, position):
        if (position.x < self.xMin or position.x >= self.xMax or
                position.y < self.yMin or position.y >= self.yMax):
            return TileContent.Empty

        x = position.x - self.xMin
        y = position.y - self.yMin
        return self.tiles[x][y].TileContent

    def initMapSize(self):
        if self.tiles is not None:
            self.xMax = self.xMin + len(self.tiles)
            self.yMax = self.yMin + len(self.tiles[0])
            self.visibleDistance = (self.xMax - self.xMin - 1) / 2
    
    def findTileContent(self, content):
        for row in self.tiles:
            for col in row:
                if col.TileContent == content:
                    yield col

    def get(self, x, y):
        return self.tiles[x - self.xMin][y - self.yMin]

    def deserializeMap(self, serializedMap):
        serializedMap = serializedMap[1:-2]
        rows = serializedMap.split('[')
        self.tiles = []
        for i in range(len(rows) - 1):
            self.tiles.append([])
            column = rows[i + 1].split('{')
            for j in range(len(column) - 1):
                x = i + self.xMin
                y = j + self.yMin
                # Tile is not empty
                if not column[j + 1][0] == '}':
                    infos = column[j + 1].split('}')
                    # Info may contain only tile content, but could also contain additional info for specific tile types
                    if infos[0].find(',') != -1:
                        infos = infos[0].split(',')

                    # Handle tile types
                    if TileContent(int(infos[0])) == TileContent.Resource:
                        amount_left = int(infos[1])
                        density = float(infos[2])
                        self.tiles[i].append(ResourceTile(TileContent(int(infos[0])), x, y, amount_left, density))
                    else:
                        self.tiles[i].append(Tile(TileContent(int(infos[0])), x, y))
                else:
                    self.tiles[i].append(Tile(TileContent.Empty, x, y))
