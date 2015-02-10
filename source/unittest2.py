__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runAdventurerTestCase1():
    """
    Precondition: there should be at least an adventurer card in hand.
    Test case description: play the adventurer card in hand.
    Expected result: Two additional treasure cards are added in your hand.
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
    game.players[game.whoseTurn].handCards = [enums.Card.adventurer, enums.Card.copper,
                                             enums.Card.copper, enums.Card.chapel,
                                             enums.Card.copper]

    handcardcountbefore = game.players[game.whoseTurn].handCardCount()

    treasurebefore = 0
    for i in range(0, handcardcountbefore):
        card = game.players[game.whoseTurn].handCards[i]
        if card == enums.Card.copper or card == enums.Card.silver or card == enums.Card.gold:
                    treasurebefore += 1

    dominion.playCard(0, 0, 0, 0, game)

    handcardcountafter = game.players[game.whoseTurn].handCardCount()

    treasureafter = 0
    for i in range(0, handcardcountafter):
        card = game.players[game.whoseTurn].handCards[i]
        if card == enums.Card.copper or card == enums.Card.silver or card == enums.Card.gold:
                    treasureafter += 1

    if treasurebefore == treasureafter - 2 and handcardcountbefore == handcardcountafter - 1:
        print "test case 1 for adventurer card: Passed!\n"
    else:
        print "test case 1 for adventurer card: Failed.\n"


def main(argv):

    runAdventurerTestCase1()


if __name__ == "__main__":
    main(sys.argv[1:])