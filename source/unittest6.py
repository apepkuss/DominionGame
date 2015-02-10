__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runCellarTestCase1():
    """
    Precondition: There should be at least a cellar card in hand.
    Test case description: play the cellar card in hand, and discard 2 hand cards.
    Expected result: The number of hand cards = current hand cards - 1; add one more action.
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
    game.players[game.whoseTurn].handCards = [enums.Card.cellar, enums.Card.copper,
                                             enums.Card.copper, enums.Card.chapel,
                                             enums.Card.copper]

    handcardbefore = game.players[game.whoseTurn].handCardCount()
    actionsbefore = game.numActions

    dominion.playCard(0, 3, -1, -1, game)

    handcardafter = game.players[game.whoseTurn].handCardCount()
    actionsafter = game.numActions

    if handcardbefore == handcardafter + 1 and actionsbefore == actionsafter:
        print "test case 1 for cellar card: Passed!\n"
    else:
        print "test case 1 for cellar card: Failed.\n"


def main(argv):

    runCellarTestCase1()


if __name__ == "__main__":
    main(sys.argv[1:])
