__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runGetWinnerTestCase1():
    """
    This test case is designed to test getWinner function.
    """

    # The number of players
    numPlayers = 2

    # 10 kinds of kingdom cards
    kingdomCards = [enums.Card.laboratory, enums.Card.adventurer, enums.Card.bureaucrat,
                    enums.Card.village, enums.Card.gardens, enums.Card.councilroom,
                    enums.Card.cellar, enums.Card.chancellor, enums.Card.chapel,
                    enums.Card.festival]

    randomSeed = 1

    print "Starting game."

    game = dominion.initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.whoseTurn = 0

    winners = dominion.getWinners(game.players, game)

    if len(winners) == 1 and winners[0] == 1:
        print "test case 1 for getWinner function: Passed!\n"
    else:
        print "test case 1 for getWinner function: Failed.\n"


def runGetWinnerTestCase2():
    """
    This test case is designed to test getWinner function.
    """

    # The number of players
    numPlayers = 2

    # 10 kinds of kingdom cards
    kingdomCards = [enums.Card.laboratory, enums.Card.adventurer, enums.Card.bureaucrat,
                    enums.Card.village, enums.Card.gardens, enums.Card.councilroom,
                    enums.Card.cellar, enums.Card.chancellor, enums.Card.chapel,
                    enums.Card.festival]

    randomSeed = 1

    print "Starting game."

    game = dominion.initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.whoseTurn = 1

    winners = dominion.getWinners(game.players, game)

    if len(winners) == 2:
        print "test case 2 for getWinner function: Passed!\n"
    else:
        print "test case 2 for getWinner function: Failed.\n"


def main(argv):

    runGetWinnerTestCase1()

    runGetWinnerTestCase2()


if __name__ == "__main__":
    main(sys.argv[1:])
