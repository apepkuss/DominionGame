__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def runBureaucratTestCase1():
    """
    Precondition: There should be at least a Bureaucrat card in hand.
                  The opponent has a Victory card in the hand card at least.
    Test case description: play the Bureaucrat card in hand.
    Expected result: Current player gets a silver and put it on the top of
                     the deck; and, the opponent puts a Victory card back to
                     the deck.
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
    game.players[game.whoseTurn].handCards = [enums.Card.bureaucrat, enums.Card.copper,
                                             enums.Card.copper, enums.Card.chapel,
                                             enums.Card.copper]

    for i in range(0, len(game.players)):
        if i != game.whoseTurn:
            game.players[i].handCards[0] = enums.Card.province

    counterbefore = 0
    victoriesbefore = 0
    decksbefore = 0
    for i in range(0, len(game.players)):
            if i != game.whoseTurn:
                for j in range(0, game.players[i].handCardCount()):
                    if enums.Card.estate <= game.players[i].handCards[j] <= enums.Card.province:
                        victoriesbefore += 1

                counterbefore += game.players[i].handCardCount()
                decksbefore += game.players[i].deckCount()

    handcardbefore = game.players[game.whoseTurn].handCardCount()
    silverbefore = game.players[game.whoseTurn].silver
    deckbefore = game.players[game.whoseTurn].deckCount()


    dominion.playCard(0, 0, 0, 0, game)

    counterafter = 0
    victoriesafter = 0
    decksafter = 0
    for i in range(0, len(game.players)):
            if i != game.whoseTurn:
                for j in range(0, game.players[i].handCardCount()):
                    if enums.Card.estate <= game.players[i].handCards[j] <= enums.Card.province:
                        victoriesafter += 1

                counterafter += game.players[i].handCardCount()
                decksafter += game.players[i].deckCount()

    handcardafter = game.players[game.whoseTurn].handCardCount()
    silverafter = game.players[game.whoseTurn].silver
    deckafter = game.players[game.whoseTurn].deckCount()

    if victoriesbefore == victoriesafter + (len(game.players) - 1) and \
                    decksbefore == decksafter - (len(game.players) - 1) and \
                    silverbefore == silverafter - 1 and \
                    deckbefore == deckafter - 1 and \
                    handcardbefore == handcardafter + 1:
        print "test case 1 for Bureaucrat card: Passed!\n"
    else:
        print "test case 1 for Bureaucrat card: Failed.\n"


def main(argv):

    runBureaucratTestCase1()


if __name__ == "__main__":
    main(sys.argv[1:])