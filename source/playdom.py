__author__ = 'liux4@onid.oregonstate.edu'

import enums
import dominion


if __name__ == "__main__":

    print "This is the main function, which is the entry of Dominion game."

    numPlayers = 2  # The number of players participating the game.
    kingdomCards = [enums.Card.adventurer, enums.Card.gardens, enums.Card.embargo,
                    enums.Card.village, enums.Card.minion, enums.Card.mine,
                    enums.Card.cutpurse, enums.Card.seahag, enums.Card.tribute,
                    enums.Card.smithy]
    randomSeed = 1  # TODO: the value should be specified from the argument of the main function.

    print "Starting game."
    gameState = dominion.initializeGame(numPlayers, kingdomCards, randomSeed)

    money = 0
    smithyPos = -1
    adventurerPos = -1
    i = 0

    numSmithies = 0
    numAdventurers = 0

    while not dominion.isGameOver(gameState):
        money = 0
        smithyPos = -1
        adventurerPos = -1

        for i in range(dominion.numHandCards(gameState)):
            if dominion.handCard(i, gameState) == enums.Card.copper:
                money += 1
            elif dominion.handCard(i, gameState) == enums.Card.silver:
                money += 2
            elif dominion.handCard(i, gameState) == enums.Card.gold:
                money += 3
            elif dominion.handCard(i, gameState) == enums.Card.smithy:
                smithyPos = i;
            elif dominion.handCard(i, gameState) == enums.Card.adventurer:
                adventurerPos = i
            # Potential Bug: here should be a else statement.

        if dominion.whoseTurn(gameState) == 0:
            if smithyPos != -1:
                print "0: smithy played from position {0:d}\n".format(smithyPos)

            dominion.playCard(smithyPos, -1, -1, -1, gameState)

            print "smithy played.\n"
            money = 0
            for i in range(dominion.numHandCards(gameState)):
                if dominion.handCard(i, gameState) == enums.Card.copper:
                    dominion.playCard(i, -1, -1, -1, gameState)
                    money += 1
                elif dominion.handCard(i, gameState) == enums.Card.silver:
                    dominion.playCard(i, -1, -1, -1, gameState)
                    money += 2
                elif dominion.handCard(i, gameState) == enums.Card.gold:
                    dominion.playCard(i, -1, -1, -1, gameState)
                    money += 3

            if money >= 8:
                print "0: bought province\n"
                dominion.buyCard(enums.Card.province, gameState)
            elif money >= 6:
                print "0: bought gold\n"
                dominion.buyCard(enums.Card.gold, gameState)
            elif (money >= 4) and (numSmithies < 2):
                print "0: bought smithy\n"
                dominion.buyCard(enums.Card.smithy, gameState)
                numSmithies += 1
            elif money >= 3:
                print "0: bought silver\n"
                dominion.buyCard(enums.Card.silver, gameState)

            print "0: end turn\n"
            dominion.endTurn(gameState)

        else:

            if adventurerPos != -1:
                print "1: adventurer played from position {0:d}\n".format(adventurerPos)

                dominion.playCard(adventurerPos, -1, -1, -1, gameState)

                money = 0
                for i in range(dominion.numHandCards(gameState)):

                    if dominion.handCard(i, gameState) == enums.Card.copper:
                        dominion.playCard(i, -1, -1, -1, gameState)
                        money += 1
                    elif dominion.handCard(i, gameState) == enums.Card.silver:
                        dominion.playCard(i, -1, -1, -1, gameState)
                        money += 2
                    elif dominion.handCard(i, gameState) == enums.Card.gold:
                        dominion.playCard(i, -1, -1, -1, gameState)
                        money += 3

            if money >= 8:
                print "1: bought province\n"
                dominion.buyCard(enums.Card.province, gameState)
            elif (money >= 6) and (numAdventurers < 2):
                print "1: bought adventurer\n"
                dominion.buyCard(enums.Card.adventurer, gameState)
                numAdventurers += 1
            elif money >= 6:
                print "1: bought gold\n"
                dominion.buyCard(enums.Card.gold, gameState)
            elif money >= 3:
                print "1: bought silver\n"
                dominion.buyCard(enums.Card.silver, gameState)

            print "1: endTurn\n"
            dominion.endTurn(gameState)

        print "Player 0: {0:d}\nPlayer 1: {1:d}\n".format(dominion.scoreFor(0, gameState), dominion.scoreFor(1, gameState))

    print "Finished game.\n"
    print "Player 0: {0:d}\nPlayer 1: {1:d}\n".format(dominion.scoreFor(0, gameState), dominion.scoreFor(1, gameState))












