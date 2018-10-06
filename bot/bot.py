from helper import *
import bot.implementation
from bot.pathfinding import Pathfinding
from helper.mapHelper import MapHelper
from bot.pathingActions import PathingActions

class Bot:
    def __init__(self):
        self.pathfinding = Pathfinding()

    def before_turn(self, PlayerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param PlayerInfo: Your bot's current state.
        """
        self.PlayerInfo = PlayerInfo

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """
        self.pathfinding.setMap(gameMap)

        # If player is full, move back to his home.
        if self.PlayerInfo.CarriedResources == self.PlayerInfo.CarryingCapacity:
            return self.createMoveToHome()
        # Else, if you can buy an upgrade, do it.
        # elif Store.canPlayerBuyUpgrade(self.PlayerInfo, UpgradeType.CollectingSpeed):
        else:
            return self.mineClosest(gameMap, visiblePlayers)
    
    def mineClosest(self, gameMap, visiblePlayers):
        choices = gameMap.findTileContent(TileContent.Resource)
        choices = bot.implementation.sort_by_distance(choices, self.PlayerInfo.Position)

        while len(choices) > 0:
            closest = choices.pop(0)
            path = self.pathfinding.solve(self.PlayerInfo.Position, closest.Position)

            if path is not None:
                direction = MapHelper.getMoveTowards(self.PlayerInfo.Position, path[0])
                return PathingActions.doActionInPath(gameMap, self.PlayerInfo.Position, direction, TileContent.Resource, create_collect_action)

        print("NO PATH POSSIBLE FIX THIS")
        return self.createMoveToHome()

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass

    # Move the player back to his home 
    def createMoveToHome(self):
        path = self.pathfinding.solve(self.PlayerInfo.Position, self.PlayerInfo.HouseLocation)
        direction = MapHelper.getMoveTowards(self.PlayerInfo.Position, path[0])
        return create_move_action(direction)

    def goToAndDo(self, gameMap, to, action):
        # First we align the player with the y position of his house.
        direction = MapHelper.getMoveTowards(self.PlayerInfo.Position, to)

        if MapHelper.isNextTo(self.PlayerInfo.Position, to):
            return action(direction)
        else:
            return PathingActions.doActionInPath(gameMap, self.PlayerInfo.Position, direction, TileContent.wall, create_attack_action)

