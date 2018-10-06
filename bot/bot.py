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
        print("Position: %r" % self.PlayerInfo.Position)

        # If player is full, move back to his home.
        if self.PlayerInfo.CarriedResources >= self.PlayerInfo.CarryingCapacity:
            print("I'm full! Going back home...")
            action = self.createMoveToHome()
        else:
            print("Not full, going to mine...")
            action = self.mineClosest(gameMap, visiblePlayers)
        
        print("Action: %r" % action)
        return action
    
    def mineClosest(self, gameMap, visiblePlayers):
        choices = gameMap.findTileContent(TileContent.Resource)
        paths = [self.pathfinding.solve(self.PlayerInfo.Position, choice.Position) for choice in choices]
        paths = [path for path in paths if path is not None]
        paths.sort(key = lambda path: len(path))

        if len(paths) == 0:
            print("NO PATH POSSIBLE FIX THIS")
            return self.createMoveToHome()
        else:
            path = paths[0]
            print("Found path to resource at: %r" % path[-1])
            print("Path: %r" % path)

            direction = MapHelper.getMoveTowards(self.PlayerInfo.Position, path[0])
            return PathingActions.doActionInPath(gameMap, self.PlayerInfo.Position, direction, TileContent.Resource, create_collect_action)
                
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

