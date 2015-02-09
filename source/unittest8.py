__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runFestivalTestCase1():
    """
    Precondition: There should be at least a festival card in hand.
    Test case description: play the festival card in hand.
    Expected result: +2 actions, +2 coins, and +1 Buy.
    """

    # The number of players
    numPlayers = 2

    # 10 kinds of kingdom cards
    kingdomCards = [enums.Card.market, enums.Card.adventurer, enums.Card.militia,
                    enums.Card.mine, enums.Card.moat, enums.Card.remodel,
                    enums.Card.smithy, enums.Card.village, enums.Card.woodcutter,
                    enums.Card.workshop]

    randomSeed = 1

    print "Starting game."

    game = dominion.initialize(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.whoseTurn = 0
    game.players[game.whoseTurn].handCards = [enums.Card.festival, enums.Card.bureaucrat,
                                             enums.Card.adventurer, enums.Card.chapel,
                                             enums.Card.cellar]

    actionsbefore = game.numActions
    buysbefore = game.numBuys
    coinsbefore = game.players[game.whoseTurn].coins

    dominion.playCard(0, -1, -1, -1, game)

    actionsafter = game.numActions
    buysafter = game.numBuys
    coinsafter = game.players[game.whoseTurn].coins

    if actionsbefore == actionsafter - 1 and buysbefore == buysafter - 1 and coinsbefore == coinsafter - 2:
        print "test case 1 for festival card: Passed!\n"
    else:
        print "test case 1 for festival card: Failed.\n"


def main(argv):

    runFestivalTestCase1()


if __name__ == "__main__":
    main(sys.argv[1:])
