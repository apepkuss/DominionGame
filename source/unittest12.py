__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runVillageTestCase1():
    """
    Precondition: There should be at least a village card in hand.
    Test case description: play the village card in hand.
    Expected result: +2 actions and +1 Card.
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
    game.players[game.whoseTurn].handCards = [enums.Card.village, enums.Card.bureaucrat,
                                             enums.Card.adventurer, enums.Card.chapel,
                                             enums.Card.cellar]

    actionsbefore = game.numActions
    handsizebefore = game.players[game.whoseTurn].handCardCount()

    dominion.playCard(0, -1, -1, -1, game)

    actionsafter = game.numActions
    handsizeafter = game.players[game.whoseTurn].handCardCount()

    if actionsbefore == actionsafter - 1 and handsizebefore == handsizeafter:
        print "test case 1 for village card: Passed!\n"
    else:
        print "test case 1 for village card: Failed.\n"


def main(argv):

    runVillageTestCase1()


if __name__ == "__main__":
    main(sys.argv[1:])
