__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runLaboratoryTestCase1():
    """
    Precondition: There should be at least a laboratory card in hand.
    Test case description: play the laboratory card in hand.
    Expected result: +2 cards in hand and +1 action.
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
    game.players[game.whoseTurn].handCards = [enums.Card.laboratory, enums.Card.bureaucrat,
                                             enums.Card.adventurer, enums.Card.chapel,
                                             enums.Card.cellar]

    actionsbefore = game.numActions
    handsizebefore = game.players[game.whoseTurn].handCardCount()

    dominion.playCard(0, -1, -1, -1, game)

    actionsafter = game.numActions
    handsizeafter = game.players[game.whoseTurn].handCardCount()

    if actionsbefore == actionsafter - 1 and handsizebefore == handsizeafter - 1:
        print "test case 1 for laboratory card: Passed!\n"
    else:
        print "test case 1 for laboratory card: Failed.\n"


def main(argv):

    runLaboratoryTestCase1()


if __name__ == "__main__":
    main(sys.argv[1:])
