class Store:
    upgrade_costs = (0, 10000, 15000, 25000, 50000, 100000)

    @staticmethod
    def canPlayerBuyUpgrade(player, upgradeName):
        moneyOfPlayer = player.TotalResources
        currentLevelOfPlayer = player.UpgradeLevels[upgradeName]

        return currentLevelOfPlayer < 5 and moneyOfPlayer >= Store.upgrade_costs[ currentLevelOfPlayer + 1 ]


    @staticmethod
    def canPlayerBuyItem(player, upgradeName):
        moneyOfPlayer = player.TotalResources
        currentLevelOfPlayer = player.UpgradeLevels[upgradeName]

        return currentLevelOfPlayer < 5 and moneyOfPlayer >= Store.upgrade_costs[ currentLevelOfPlayer + 1 ]