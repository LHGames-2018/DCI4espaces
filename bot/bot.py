from helper import *
import bot.implementation
from bot.pathfinding import Pathfinding

class Bot:
    def __init__(self):
        self.pathfinding = Pathfinding()

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.PlayerInfo = playerInfo
        self.persistent_map = gamemap.load_persistent_map()

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """
        self.persistent_map.update(gameMap, self.PlayerInfo.HouseLocation)
        self.pathfinding.setMap(self.persistent_map)
        move_destination = bot.implementation.get_closest(gameMap.findTileContent(TileContent.Resource), self.PlayerInfo.Position)
        return create_move_action(Point(-1, 0))

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
