__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runSmithyTestCase1():
    """
    Precondition: There should be at least a smithy card in hand.
    Test case description: play the smithy card in hand.
    Expected result: your handsize +3.
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
    game.players[game.whoseTurn].handCards = [enums.Card.smithy, enums.Card.bureaucrat,
                                             enums.Card.adventurer, enums.Card.chapel,
                                             enums.Card.cellar]

    handsizebefore = game.players[game.whoseTurn].handCardCount()

    dominion.playCard(0, -1, -1, -1, game)

    handsizeafter = game.players[game.whoseTurn].handCardCount()

    if handsizebefore == handsizeafter - 2:
        print "test case 1 for smithy card: Passed!\n"
    else:
        print "test case 1 for smithy card: Failed.\n"


def main(argv):

    runSmithyTestCase1()


if __name__ == "__main__":
    main(sys.argv[1:])
