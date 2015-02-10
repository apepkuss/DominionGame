__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runBuycardTestCase1():
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

    originalcoins = game.players[game.whoseTurn].coins
    game.players[game.whoseTurn].coins = 0

    result = dominion.buyCard(enums.Card.province, game)

    if result == -1 and game.error == "You do not have enough money to buy that.\n":
        print "test case 1 for buyCard function without enough coins to buy: Passed!\n"
    else:
        print "test case 1 for buyCard function without enough coins to buy: Failed.\n"

    game.players[game.whoseTurn].coins = originalcoins
    game.error = ""

    provincecount = game.supplies.provinceCount
    game.supplies.provinceCount = 0

    result = dominion.buyCard(enums.Card.province, game)

    if result == -1 and game.error == "There are not any of that type of card left\n":
        print "test case 1 for playCard function without enough supply: Passed!\n"
    else:
        print "test case 1 for playCard function without enough supply: Failed.\n"

    game.supplies.provinceCount = provincecount
    game.error = ""

    numbuy = game.numBuys
    game.numBuys = 0
    coins = game.players[game.whoseTurn].coins
    game.players[game.whoseTurn].coins = 100

    result = dominion.buyCard(enums.Card.province, game)

    if result == -1 and game.error == "You do not have any buys left\n":
        print "test case 1 for playCard function with numBuys = 0: Passed!\n"
    else:
        print "test case 1 for playCard function with numBuys = 0: Failed.\n"

    game.numBuys = numbuy
    game.players[game.whoseTurn].coins = coins
    game.error = ""

    current = game.whoseTurn
    result = dominion.endTurn(game)
    next = game.whoseTurn

    if result == 0 and next == (current + 1) % len(game.players):
        print "test case 1 for endTurn function: Passed!\n"
    else:
        print "test case 1 for endTurn function: Failed.\n"

    result = dominion.isGameOver(game)

    if not result:
        print "test case 1 for isGameOver function: Passed!\n"
    else:
        print "test case 1 for isGameOver function: Failed.\n"

    provinces = game.supplies.provinceCount
    game.supplies.provinceCount = 0

    result = dominion.isGameOver(game)
    if result:
        print "test case 2 for isGameOver function: Passed!\n"
    else:
        print "test case 2 for isGameOver function: Failed.\n"

    game.supplies.provinceCount = provinces

    game.supplies.curseCount = 0
    game.supplies.estateCount = 0
    game.supplies.duchyCount = 0
    game.supplies.provinceCount = 0
    game.supplies.copperCount = 0
    game.supplies.silverCount = 0
    game.supplies.goldCount = 0

    result = dominion.isGameOver(game)
    if result:
        print "test case 3 for isGameOver function: Passed!\n"
    else:
        print "test case 3 for isGameOver function: Failed.\n"


def main(argv):

    runBuycardTestCase1()


if __name__ == "__main__":
    main(sys.argv[1:])
