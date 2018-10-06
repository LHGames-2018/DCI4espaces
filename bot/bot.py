from helper import *
from bot.implementation import *
from bot.decision import decision
from bot.pathfinding import Pathfinding
from helper.mapHelper import MapHelper
from bot.pathingActions import PathingActions
import random

class Bot:
    def __init__(self):
        self.pathfinding = Pathfinding()

    def before_turn(self, PlayerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param PlayerInfo: Your bot's current state.
        """
        self.PlayerInfo = PlayerInfo
        self.persistent_map = gamemap.load_persistent_map()

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """
        self.persistent_map.update(gameMap, self.PlayerInfo.HouseLocation)
        self.pathfinding.setMap(self.persistent_map)
        print("Position: %r" % self.PlayerInfo.Position)
        print("Total Resources:" + str(self.PlayerInfo.TotalResources))

        # Tuer un ennemi s'il est dans une case adjacente
        res = self.killOtherPlayerWhenClose(gameMap, visiblePlayers)
        if res != None:
            return res

        # If player is full, move back to his home.
        if self.PlayerInfo.CarriedResources >= self.PlayerInfo.CarryingCapacity:
            print("I'm full! Going back home...")
            action = self.createMoveToHome()
        elif Store.canPlayerBuyUpgrade(self.PlayerInfo, UpgradeType.CollectingSpeed):
            print("Going for an upgrade: CollectingSpeed")
            return self.buyUpgrade(UpgradeType.CollectingSpeed)
        elif Store.canPlayerBuyUpgrade(self.PlayerInfo, UpgradeType.CarryingCapacity):
            print("Going for an upgrade: CarryingCapacity")
            return self.buyUpgrade(UpgradeType.CarryingCapacity)
        else:
            print("Not full, going to mine...")
            action = self.mineClosest(self.persistent_map, visiblePlayers)
        
        print("Action: %r" % action)
        return action
    
    def killOtherPlayerWhenClose(self, gameMap, visiblePlayers):
        if len(visiblePlayers) > 0:
            enemy = get_closest(visiblePlayers, self.PlayerInfo.Position)

            if MapHelper.isNextTo(enemy.Position, self.PlayerInfo.Position):
                print("Another player has moved too close! Attack him!")
                p = MapHelper.getMoveTowards(self.PlayerInfo.Position, enemy.Position)

                return create_attack_action(p)

            # Quand en dedans d'un certain rayon
            elif MapHelper.isCloseTo(enemy.Position, self.PlayerInfo.Position):
                print("Another player is close. Move towards him in order to attack!")
                
                path = self.pathfinding.solve(self.PlayerInfo.Position, enemy.Position)

                if path is not None:
                    direction = MapHelper.getMoveTowards(self.PlayerInfo.Position, path[0])
                    return create_move_action(direction)
                else:
                    print("Problem: No path to enemy!!!")

        print("No enemy to attack.")
        return None

    def exploreAround(self, gameMap, visiblePlayers):
        # Quand il y a pas de chemin: Explorer en allant dans une direction arbitraire
        x_ou_y = random.randint(0,2)
        # 1/3 chance d'aller vers la droite, sinon on va vers le haut.
        p = Point(0, 1) if x_ou_y == 1 else Point(1, 0)

        path = self.pathfinding.solve(self.PlayerInfo.Position, self.PlayerInfo.Position + p)

        if path is not None:
            direction = MapHelper.getMoveTowards(self.PlayerInfo.Position, path[0])
            return PathingActions.doActionInPath(gameMap, self.PlayerInfo.Position, direction, TileContent.Resource, create_collect_action)

        # Pas de chemin possible! Essayer un autre direction arbitraire
        x_ou_y = random.randint(0,2)
        # 1/3 chance d'aller vers le haut, sinon on va vers la gauche.
        p = Point(1, 0) if x_ou_y == 1 else Point(0, -1)

        path = self.pathfinding.solve(self.PlayerInfo.Position, self.PlayerInfo.Position + p)

        if path is not None:
            direction = MapHelper.getMoveTowards(self.PlayerInfo.Position, path[0])
            return PathingActions.doActionInPath(gameMap, self.PlayerInfo.Position, direction, TileContent.Resource, create_collect_action)

        print("NO PATH POSSIBLE FIX THIS")
        return self.createMoveToHome()

    def mineClosest(self, gameMap, visiblePlayers):
        choices = gameMap.findTileContent(TileContent.Resource)
        paths = [self.pathfinding.solve(self.PlayerInfo.Position, choice.Position) for choice in choices]
        paths = [path for path in paths if path is not None]
        paths.sort(key = lambda path: len(path))

        if len(paths) == 0:
            print("NO PATH POSSIBLE FIX THIS")
            return self.exploreAround(gameMap, visiblePlayers)
        else:
            path = paths[0]
            target_node = path[-1]
            print("Found path to resource at: %r" % target_node)

            pathThroughHouse = self.findPathThroughHouse(target_node)

            if pathThroughHouse is not None and len(pathThroughHouse) == len(path):
                print("Found a better mining path that goes through my house! :D ")
                path = pathThroughHouse

            print("Path: %r" % path)

            next_node = path[0]
            direction = MapHelper.getMoveTowards(self.PlayerInfo.Position, next_node)
            return PathingActions.doActionInPath(gameMap, self.PlayerInfo.Position, direction, TileContent.Resource, create_collect_action)
    
    def findPathThroughHouse(self, target):
        playerToHouse = self.pathfinding.solve(self.PlayerInfo.Position, self.PlayerInfo.HouseLocation)
        if playerToHouse is None:
            return None
        
        houseToTarget = self.pathfinding.solve(self.PlayerInfo.HouseLocation, target)
        if houseToTarget is None:
            return None
        
        return playerToHouse + houseToTarget

    def callDecision(self, gameMap, visiblePlayers):
        # On prend tout ce qui existe de pertinent, donc on exclut les murs et la lave
        # parce que c'est au pathfinder de dealer avec ça pour les éviter. 
        players = gameMap.findTileContent(TileContent.Player)   # FIXME PROBABLEMENT BROKE, utiliser visiblePlayers
        houses = gameMap.findTileContent(TileContent.House)
        resource = gameMap.findTileContent(TileContent.Resource)
        shop = gameMap.findTileContent(TileContent.Shop)

        liste = []
        liste.extend(players)
        liste.extend(houses)
        liste.extend(resource)
        liste.extend(shop)

        best_tuile = decision(liste, self.PlayerInfo)

        #choices = bot.implementation.sort_by_distance(choices, self.PlayerInfo.Position)

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
        direction = MapHelper.getMoveTowards(self.PlayerInfo.Position, to)

        if MapHelper.isNextTo(self.PlayerInfo.Position, to):
            return action(direction)
        else:
            return PathingActions.doActionInPath(gameMap, self.PlayerInfo.Position, direction, TileContent.Wall, create_attack_action)

    def findClosest(self, gameMap, tileContent):
        choices = gameMap.findTileContent(tileContent)
        return get_closest(choices, self.PlayerInfo.Position)

    def buyUpgrade(self, upgradeType): 
        if MapHelper.isOn(self.PlayerInfo.Position, self.PlayerInfo.HouseLocation):
            return create_upgrade_action(UpgradeType.CollectingSpeed)
        else:
            return self.createMoveToHome() 

