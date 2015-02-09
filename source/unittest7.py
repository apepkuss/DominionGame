__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runChancellorTestCase1():
    """
    Precondition: There should be at least a chancellor card in hand.
    Test case description: play the cellar card in hand, and discard 2 hand cards.
    Expected result: The number of hand cards = current hand cards - 1; add one more action.
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
    game.players[game.whoseTurn].handCards = [enums.Card.chancellor, enums.Card.bureaucrat,
                                             enums.Card.adventurer, enums.Card.chapel,
                                             enums.Card.cellar]

    deckbefore = game.players[game.whoseTurn].deckCount()
    discardbefore = game.players[game.whoseTurn].discardCardCount()
    coinsbefore = game.players[game.whoseTurn].coins

    dominion.playCard(0, -1, -1, -1, game)

    deckafter = game.players[game.whoseTurn].deckCount()
    discardafter = game.players[game.whoseTurn].discardCardCount()
    coinsafter = game.players[game.whoseTurn].coins

    if deckafter == 0 and discardafter == deckbefore + discardbefore + 1 and coinsbefore == coinsafter - 2:
        print "test case 1 for chancellor card: Passed!\n"
    else:
        print "test case 1 for chancellor card: Failed.\n"


def main(argv):

    runChancellorTestCase1()


if __name__ == "__main__":
    main(sys.argv[1:])
