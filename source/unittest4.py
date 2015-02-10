__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runCouncilroomTestCase1():
    """
    Precondition: there should be at least a councilroom card in hand.
    Test case description: play the councilroom card in hand.
    Expected result: The number of the hand cards of each other player increases 1.
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
    game.players[game.whoseTurn].handCards = [enums.Card.councilroom, enums.Card.copper,
                                             enums.Card.copper, enums.Card.chapel,
                                             enums.Card.copper]

    handcardbefore = game.players[game.whoseTurn].handCardCount()
    discardcountbefore = game.players[game.whoseTurn].discardCardCount()

    counterbefore = 0
    for i in range(0, len(game.players)):
        if i != game.whoseTurn:
            counterbefore += game.players[i].handCardCount()

    dominion.playCard(0, 0, 0, 0, game)

    handcardafter = game.players[game.whoseTurn].handCardCount()
    discardcardcountafter = game.players[game.whoseTurn].discardCardCount()

    counterafter = 0
    for i in range(0, len(game.players)):
        if i != game.whoseTurn:
            counterafter += game.players[i].handCardCount()

    if counterbefore == counterafter - (len(game.players) - 1) and \
                    handcardbefore == handcardafter +1 and \
                    discardcountbefore == discardcardcountafter - 1:
        print "test case 1 for councilroom card: Passed!\n"
    else:
        print "test case 1 for councilroom card: Failed.\n"


def main(argv):

    runCouncilroomTestCase1()


if __name__ == "__main__":
    main(sys.argv[1:])