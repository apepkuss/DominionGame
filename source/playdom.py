__author__ = 'liux4@onid.oregonstate.edu'

import sys
import enums
import dominion


def main(argv):

    print "This is the main function, which is the entry of Dominion game."

    # The number of players
    numPlayers = 2

    # 10 kinds of kingdom cards
    kingdomCards = [enums.Card.cellar, enums.Card.market, enums.Card.militia,
                    enums.Card.mine, enums.Card.moat, enums.Card.remodel,
                    enums.Card.smithy, enums.Card.village, enums.Card.woodcutter,
                    enums.Card.workshop]

    # randomSeed = int(argv[0])
    randomSeed = 1

    print "Starting game."

    # game = dominion.initializeGame(numPlayers, kingdomCards, randomSeed)

    game = dominion.initialize(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return -1

    game.whoseTurn = 0
    game.players[game.whoseTurn].handCards = [enums.Card.bureaucrat, enums.Card.market,
                                             enums.Card.militia, enums.Card.mine,
                                             enums.Card.moat]

    dominion.playCard(0, 0, 0, 0, game)

    # money = 0
    # smithyPos = -1
    # adventurerPos = -1

    numSmithies = 0
    numAdventurers = 0

    while not dominion.isGameOver(game):
        money = 0
        smithyPos = -1
        adventurerPos = -1

        for i in range(game.players[game.whoseTurn].handCardCount()):
            if game.players[game.whoseTurn].handCards[i] == enums.Card.copper:
                money += 1
            elif game.players[game.whoseTurn].handCards[i] == enums.Card.silver:
                money += 2
            elif game.players[game.whoseTurn].handCards[i] == enums.Card.gold:
                money += 3
            elif game.players[game.whoseTurn].handCards[i] == enums.Card.smithy:
                smithyPos = i
            elif game.players[game.whoseTurn].handCards[i] == enums.Card.adventurer:
                adventurerPos = i
            # Potential Bug: here should be a else statement.

        if dominion.whoseTurn(game) == 0:
            if smithyPos != -1:
                print "0: smithy played from position {0:d}\n".format(smithyPos)

            dominion.playCard(smithyPos, -1, -1, -1, game)

            print "smithy played.\n"
            money = 0
            for i in range(dominion.numHandCards(game)):
                if dominion.handCard(i, game) == enums.Card.copper:
                    dominion.playCard(i, -1, -1, -1, game)
                    money += 1
                elif dominion.handCard(i, game) == enums.Card.silver:
                    dominion.playCard(i, -1, -1, -1, game)
                    money += 2
                elif dominion.handCard(i, game) == enums.Card.gold:
                    dominion.playCard(i, -1, -1, -1, game)
                    money += 3

            if money >= 8:
                print "0: bought province\n"
                result = dominion.buyCard(enums.Card.province, game)
                assert (result != -1), "The returned value of buyCard should not be -1."
            elif money >= 6:
                print "0: bought gold\n"
                result = dominion.buyCard(enums.Card.gold, game)
                assert (result != -1), "The returned value of buyCard should not be -1."
            elif (money >= 4) and (numSmithies < 2):
                print "0: bought smithy\n"
                result = dominion.buyCard(enums.Card.smithy, game)
                assert (result != -1), "The returned value of buyCard should not be -1."
                numSmithies += 1
            elif money >= 3:
                print "0: bought silver\n"
                result = dominion.buyCard(enums.Card.silver, game)
                assert (result != -1), "The returned value of buyCard should not be -1."

            print "0: end turn\n"
            dominion.endTurn(game)

        else:

            if adventurerPos != -1:
                print "1: adventurer played from position {0:d}\n".format(adventurerPos)

                dominion.playCard(adventurerPos, -1, -1, -1, game)

                money = 0
                for i in range(dominion.numHandCards(game)):

                    if dominion.handCard(i, game) == enums.Card.copper:
                        dominion.playCard(i, -1, -1, -1, game)
                        money += 1
                    elif dominion.handCard(i, game) == enums.Card.silver:
                        dominion.playCard(i, -1, -1, -1, game)
                        money += 2
                    elif dominion.handCard(i, game) == enums.Card.gold:
                        dominion.playCard(i, -1, -1, -1, game)
                        money += 3

            if money >= 8:
                print "1: bought province\n"
                dominion.buyCard(enums.Card.province, game)
            elif (money >= 6) and (numAdventurers < 2):
                print "1: bought adventurer\n"
                dominion.buyCard(enums.Card.adventurer, game)
                numAdventurers += 1
            elif money >= 6:
                print "1: bought gold\n"
                dominion.buyCard(enums.Card.gold, game)
            elif money >= 3:
                print "1: bought silver\n"
                dominion.buyCard(enums.Card.silver, game)

            print "1: endTurn\n"
            dominion.endTurn(game)

        print "Player 0: {0:d}\nPlayer 1: {1:d}\n".format(dominion.scoreFor(0, game), dominion.scoreFor(1, game))

    print "Finished game.\n"
    print "Player 0: {0:d}\nPlayer 1: {1:d}\n".format(dominion.scoreFor(0, game), dominion.scoreFor(1, game))


if __name__ == "__main__":
    main(sys.argv[1:])