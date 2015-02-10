__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runPlaycardTestCase1():
    """
    This test case is designed to test invalid phase and the number of actions of the game.
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

    originalphase = game.phase
    game.phase = enums.GamePhase.buy

    result = dominion.playCard(0, -1, -1, -1, game)

    if result == -1 and game.error == "Not allowed to play card in non-action phase.\n":
        print "test case 1 for playCard function: Passed!\n"
    else:
        print "test case 1 for playCard function: Failed.\n"

    game.phase = originalphase
    game.error = ""

    originalactions = game.numActions
    game.numActions = 0

    result = dominion.playCard(0, -1, -1, -1, game)

    if result == -1 and game.error == "Not allowed to play card when the number of actions is less than 1.\n":
        print "test case 1 for playCard function with numActions = 0: Passed!\n"
    else:
        print "test case 1 for playCard function with numActions = 0: Failed.\n"

    game.numActions = originalactions


def runPlaycardTestCase2():
    """
    This test case is designed to check how to deal with playing non-action card
    in action phase when there is action card.
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

    game.phase = enums.GamePhase.action
    game.whoseTurn = 0
    game.players[game.whoseTurn].handCards = [enums.Card.copper, enums.Card.bureaucrat,
                                             enums.Card.adventurer, enums.Card.chapel,
                                             enums.Card.cellar]

    result = dominion.playCard(0, -1, -1, -1, game)

    if result == -1 and game.error == "This is an invalid card.\n":
        print "test case 2 for playCard function when playing non-action cards: Passed!\n"
    else:
        print "test case 2 for playCard function when playing non-action cards: Failed.\n"

    game.error = ""
    game.players[game.whoseTurn].handCards[0] = 20

    result = dominion.playCard(0, -1, -1, -1, game)

    if result == -1 and game.error == "This is an invalid card.\n":
        print "test case 2 for playCard function when playing an invalid card: Passed!\n"
    else:
        print "test case 2 for playCard function when playing an invalid card: Failed.\n"


def main(argv):

    runPlaycardTestCase1()

    runPlaycardTestCase2()


if __name__ == "__main__":
    main(sys.argv[1:])
