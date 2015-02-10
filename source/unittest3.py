__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runFeastTestCase1():
    """
    Precondition: there should be at least a feast card in hand.
    Test case description: play the feast card in hand.
    Expected result: The gained card goes into the Discard pile.
    """

    # The number of players
    numPlayers = 2

    # 10 kinds of kingdom cards
    kkingdomCards = [enums.Card.laboratory, enums.Card.adventurer, enums.Card.bureaucrat,
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
    game.players[game.whoseTurn].handCards = [enums.Card.feast, enums.Card.copper,
                                             enums.Card.copper, enums.Card.chapel,
                                             enums.Card.copper]

    discardcountbefore = game.players[game.whoseTurn].discardCardCount()

    dominion.playCard(0, 1, 0, 0, game)

    discardcardcountafter = game.players[game.whoseTurn].discardCardCount()

    if discardcountbefore == discardcardcountafter - 1:
        print "test case 1 for feast card: Passed!\n"
    else:
        print "test case 1 for feast card: Failed.\n"


def runFeastTestCase2():
    """
    Precondition: 1. There should be at least a feast card in hand.
                  2. The estate pile has no cards.
    Test case description: Play the feast card in hand and try to buy
                           a estate card.
    Expected result: Return the specified error message.
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

    # precondition 1
    game.players[game.whoseTurn].handCards = [enums.Card.feast, enums.Card.copper,
                                             enums.Card.copper, enums.Card.chapel,
                                             enums.Card.copper]
    # precondition 2
    game.supplies.estateCount = 0

    result = dominion.playCard(0, 1, 0, 0, game)

    if result == -1 and game.error == "None of that card left!":
        print "test case 2 for feast card: Passed!\n"
    else:
        print "test case 2 for feast card: Failed.\n"


def runFeastTestCase3():
    """
    Precondition: 1. There should be at least a feast card in hand.
                  2. The coins of the player are less then the cost
                     of a estate card.
    Test case description: Play the feast card in hand and try to buy
                           a province card.
    Expected result: Return the specified error message.
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

    # precondition 1
    game.players[game.whoseTurn].handCards = [enums.Card.feast, enums.Card.laboratory,
                                             enums.Card.estate, enums.Card.chapel,
                                             enums.Card.village]
    # precondition 2
    game.players[game.whoseTurn].coins = 1

    result = dominion.playCard(0, 3, 0, 0, game)

    if result == -1 and game.error == "That card is too expensive!":
        print "test case 3 for feast card: Passed!\n"
    else:
        print "test case 3 for feast card: Failed.\n"



def main(argv):

    runFeastTestCase1()

    runFeastTestCase2()

    runFeastTestCase3()


if __name__ == "__main__":
    main(sys.argv[1:])