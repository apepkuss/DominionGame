__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runChapelTestCase1():
    """
    Precondition: there are at least two chapel cards in hand.
    Test case description: play one of the chapel cards in hand.
    Expected result: trash a different Chapel card when that card were in your hand.
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
    game.players[game.whoseTurn].handCards = [enums.Card.chapel, enums.Card.councilroom,
                                             enums.Card.gardens, enums.Card.chancellor,
                                             enums.Card.chapel]

    trashsize = len(game.players[game.whoseTurn].trash)

    dominion.playCard(0, 0, 0, 0, game)

    nums = 0
    for i in range(0, len(game.players[game.whoseTurn].handCards)):
        if enums.Card.chapel == game.players[game.whoseTurn].handCards[i]:
            nums += 1

    if 0 == nums and trashsize == len(game.players[game.whoseTurn].trash) - 1:
        print "test case 1 for chapel card: Passed!\n"
    else:
        print "test case 2 for chapel card: Failed.\n"


def runChapelTestCase2():
    """
    Precondition: there is only one chapel card in hand.
    Test case description: play the only chapel card in hand.
    Expected result: the trash size of the player has no change.
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
    game.players[game.whoseTurn].handCards = [enums.Card.chapel, enums.Card.councilroom,
                                             enums.Card.gardens, enums.Card.chancellor,
                                             enums.Card.adventurer]

    trashsize = len(game.players[game.whoseTurn].trash)

    dominion.playCard(0, 0, 0, 0, game)

    nums = 0
    for i in range(0, len(game.players[game.whoseTurn].handCards)):
        if enums.Card.chapel == game.players[game.whoseTurn].handCards[i]:
            nums += 1

    if 0 == nums and trashsize == len(game.players[game.whoseTurn].trash):
        print "test case 1 for chapel card: Passed!\n"
    else:
        print "test case 2 for chapel card: Failed.\n"


def main(argv):

    runChapelTestCase1()

    runChapelTestCase2()


if __name__ == "__main__":
    main(sys.argv[1:])