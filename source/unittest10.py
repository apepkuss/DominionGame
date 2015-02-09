__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runSeahagTestCase1():
    """
    Precondition: There should be at least a seahag card in hand.
    Test case description: play the seahag card in hand.
    Expected result: Each other player discards the top card of his deck,
                     then gains a Curse card, putting it on top of his deck.
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
    game.players[game.whoseTurn].handCards = [enums.Card.seahag, enums.Card.bureaucrat,
                                             enums.Card.adventurer, enums.Card.chapel,
                                             enums.Card.cellar]

    discardsbefore = 0
    decksbefore = 0
    for i in range(0, len(game.players)):
        if i != game.whoseTurn:
            discardsbefore += game.players[i].discardCardCount()
            decksbefore += game.players[i].deckCount()


    dominion.playCard(0, -1, -1, -1, game)


    discardsafter = 0
    decksafter = 0
    curseflag = True
    for i in range(0, len(game.players)):
        if i != game.whoseTurn:
            discardsafter += game.players[i].discardCardCount()
            decksafter += game.players[i].deckCount()
            if game.players[i].cardsInDeck[-1] != enums.Card.curse:
                curseflag = False
                break

    if discardsbefore == discardsafter - len(game.players) + 1 and decksbefore == decksafter and curseflag:
        print "test case 1 for seahag card: Passed!\n"
    else:
        print "test case 1 for seahag card: Failed.\n"


def main(argv):

    runSeahagTestCase1()


if __name__ == "__main__":
    main(sys.argv[1:])
