__author__ = 'liux4@onid.oregonstate.edu'

import enums
import sys

from math import *
import random
import helper

# APIs definition of dominion game

def initializeGame(numPlayers, kingdomCards, randomseed):
    """
    Responsible for initializing all supplies, and shuffling deck and
    drawing starting hands for all players.  Check that 10 cards selected
    are in fact (different) kingdom cards, and that numPlayers is valid.

    :param numPlayers:
    :param kingdomCards:
    :param randomseed:
    :return:
    """

    # instantiate an object of GameState and set the number of players
    game = enums.GameState(numPlayers)

    if len(game.error) > 0:
        return game

    # check selected kingdom cards are different
    if len(kingdomCards) != len(set(kingdomCards)):
        game.error = "There are duplicate kingdom cards in the supplies."
        return game

    # set number of Curse cards
    # 10 Curse cards in the Supply for a 2 player game,
    # 20 Curse cards for 3 players, and
    # 30 Curse cards for 4 players.
    if numPlayers == 2:
        game.supplies.curseCount = 10
    elif numPlayers == 3:
        game.supplies.curseCount = 20
    else:
        game.supplies.curseCount = 30

    # 48 Victory cards
    # After each player takes 3 Estate cards,
    # 3 or 4 player game: 12 Estate, 12 Duchy, and 12 Province cards in the Supply.
    # 2 player game: 8 Estate, 8 Duchy, and 8 Province cards in the Supply.
    if numPlayers == 2:
        game.supplies.estateCount = 8
        game.supplies.duchyCount = 8
        game.supplies.provinceCount = 8
    else:
        game.supplies.estateCount = 12
        game.supplies.duchyCount = 12
        game.supplies.provinceCount = 12

    # set number of Treasure cards
    game.supplies.copperCount = 60
    game.supplies.silverCount = 40
    game.supplies.goldCount = 30

    # set number of Kingdom cards
    game.supplies.setSupplyKingdoms(kingdomCards)

    # set deck for each player
    for i in range(0, numPlayers):
        for j in range(0, 3):
            game.players[i].cardsInDeck.append(enums.Card.estate)

        for k in range(0, 7):
            game.players[i].cardsInDeck.append(enums.Card.copper)
        game.supplies.copperCount -= 7

    # shuffle decks
    for i in range(0, numPlayers):
        result = shuffle(i, game)
        if result == -1:
            game.error += "Failed to shuffle the deck of player{0:d}.\n".format(i)
            return game

    # draw 5 cards from each player's deck
    for i in range(0, numPlayers):
        # game.players[i].handCardCount = 0
        # game.players[i].discardCardCount = 0

        # draw card
        for j in range(0, 5):
            helper.drawCard(i, game)

    # set embargo tokens to 0 for all supply piles
    # for i in range(0, int(enums.Card.treasuremap) + 1):
    #     game.embargoTokens[i] = 0

    # initialize first player's turn
    game.phase = enums.GamePhase.action
    game.playedCardCount = 0
    game.outpostPlayed = 0  # TODO: what that means?
    game.numActions = 1
    game.numBuys = 1

    # game.handCount[game.whoseTurn] = 0

    for i in range(0, len(game.players)):
        helper.updateCoins(i, game, 0)

    return game


def shuffle(player, game):
    """
    Assumes all cards are now in deck array (or hand/played):  discard is empty.

    :param player:
    :param game:
    :return:
    """

    if game.players[player].deckCount() < 1:
        game.error = "Failed to shuffle the cards on the deck of Player{0:d}. The deck is empty."
        return -1

    try:
        random.shuffle(game.players[player].cardsInDeck)
    except:
        game.error = "Unexpected error: " + sys.exc_info()[0]
        return -1

    return 0


def playCard(handPos, choice1, choice2, choice3, game):
    """
    Play card with index handPos from current player's hand

    :param handPos: the index of the card to play
    :param choice1:
    :param choice2:
    :param choice3:
    :param game:
    :return:
    """

    #  check if it is the right phase
    if game.phase != 0:
        game.error = "Not allowed to play card in non-action phase.\n"
        return -1

    # check if player has enough actions
    if game.numActions < 1:
        game.error = "Not allowed to play card when the number of actions is less than 1.\n"
        return -1

    # get card played
    card = handCard(handPos, game)

    # check if selected card is an action
    if card > enums.Card.village:
        game.error = "This is an invalid card.\n"
        return -1
    elif card < enums.Card.adventurer or card > enums.Card.village or card == enums.Card.gardens:
        for i in range(0, len(game.players)):
            if i != handPos \
                    and enums.Card.adventurer <= game.players[game.whoseTurn].handCards[i] <= enums.Card.village \
                    and card != enums.Card.gardens:
                game.error = "Play action cards first."
                return -1

    # play card
    coinbonus = 0  # tracks coins gain from actions
    if helper.cardEffect(card, choice1, choice2, choice3, game, handPos, coinbonus) < 0:
        return -1

    # reduce number of actions
    game.numActions -= 1

    # update coins (Treasure cards may be added with card draws)
    helper.updateCoins(game.whoseTurn, game, coinbonus)

    return 0


def buyCard(supplyPos, game):
    """
    Buy card with supply index supplyPos
    :param supplyPos:
    :param game:
    :return:
    """

    print "Entering buyCard...\n"

    who = game.whoseTurn

    if game.numBuys < 1:
        game.error = "You do not have any buys left\n"
        return -1

    elif supplyCount(supplyPos, game) < 1:
        game.error = "There are not any of that type of card left\n"
        return -1

    elif game.players[game.whoseTurn].coins < helper.getCost(supplyPos):
        game.error = "You do not have enough money to buy that.\n"
        return -1

    else:
        game.phase = 1
        result = helper.gainCard(supplyPos, game, 0, who)

        if result != 0:
            return result

        # pay for the new card
        game.players[game.whoseTurn].coins -= helper.getCost(supplyPos)
        game.numBuys -= 1

    return 0


def numHandCards(game):
    """
    Compute the number of the cards current player has in hand
    :param game:
    :return:
    """
    return game.players[game.whoseTurn].handCardCount()


def handCard(handPos, game):
    """
    Return the value of indexed card in player's hand
    :param handPos:
    :param game:
    :return:
    """
    return game.players[game.whoseTurn].handCards[handPos]


def supplyCount(card, game):
    """
    Return the number of given card are left in supply
    :param card:
    :param game:
    :return:
    """

    # curse card
    if card == enums.Card.curse:
        return game.supplies.curseCount

    # Victory cards
    if card == enums.Card.estate:
        return game.supplies.estateCount
    elif card == enums.Card.duchy:
        return game.supplies.duchyCount
    elif card == enums.Card.province:
        return game.supplies.provinceCount

    # Treasure cards
    if card == enums.Card.copper:
        return game.supplies.copperCount
    elif card == enums.Card.silver:
        return game.supplies.silverCount
    elif card == enums.Card.gold:
        return game.supplies.goldCount

    # Kingdom cards
    if enums.Card.adventurer <= card <= enums.Card.village:
        return game.supplies.kingdoms[card]

    return -1


def fullDeckCount(player, card, game):
    """
    Here deck = hand + discard + deck
    :param player:
    :param card:
    :param game:
    :return:
    """

    count = 0

    for i in range(game.players[player].deckCount()):
        if game.players[player].cardsInDeck[i] == card:
            count += 1

    for i in range(game.players[player].handCardCount()):
        if game.players[player].handCards[i] == card:
            count += 1

    for i in range(game.players[player].discardCardCount()):
        if game.players[player].discardCards[i] == card:
            count += 1

    return count


def whoseTurn(game):
    return game.whoseTurn


def endTurn(game):
    """
    Check if current turn is over
    :param game:
    :return:
    """

    currentPlayer = whoseTurn(game)

    # Discard hand
    game.players[currentPlayer].discardCards.append(game.players[currentPlayer].handCards)
    game.players[currentPlayer].handCards = []

    # determine next player
    game.whoseTurn = (currentPlayer + 1) % len(game.players)
    game.players[game.whoseTurn].coins = 0
    game.players[game.whoseTurn].handCards = []

    # Next player draws 5 handcards
    for k in range(0, 5):
        helper.drawCard(game.whoseTurn, game)

    game.phase = 0
    game.numActions = 1
    game.numBuys = 1

    # Update money
    helper.updateCoins(game.whoseTurn, game, 0)

    return 0


def isGameOver(game):

    # The game ends at the end of any player turn when either
    # 1) the Supply pile of Province cards is empty or
    # 2) any 3 Supply piles are empty.

    if game.supplies.provinceCount == 0:
        return True

    counter = 0

    # curse card
    if game.supplies.curseCount == 0:
        counter += 1

    # Victory cards
    if game.supplies.estateCount == 0:
        counter += 1

    if game.supplies.duchyCount == 0:
        counter += 1

    if game.supplies.provinceCount == 0:
        counter += 1

    # Treasure cards
    if game.supplies.copperCount == 0:
        counter += 1

    if game.supplies.silverCount == 0:
        counter += 1

    if game.supplies.goldCount == 0:
        counter += 1

    for i in range(0, len(game.supplies.kingdoms)):
        if game.supplies.kingdoms[i] == 0:
            counter += 1

    if counter >= 3:
        return True
    else:
        return False


def scoreFor(player, game):
    """
    Return the credits the specified player gains in the game
    :param player:
    :param game:
    :return:
    """

    score = 0
    playercards = []

    playercards.extend(game.players[player].handCards)
    playercards.extend(game.players[player].discardCards)
    playercards.extend(game.players[player].cardsInDeck)

    # score from hand
    for i in range(0, len(playercards)):
        if playercards[i] == enums.Card.curse:
            score -= 1
        elif playercards[i] == enums.Card.estate:
            score += 1
        elif playercards[i] == enums.Card.duchy:
            score += 3
        elif playercards[i] == enums.Card.province:
            score += 6
        elif playercards[i] == enums.Card.gardens:
            score += (fullDeckCount(player, 0, game) / 10)

    return score


######################## UNIT TEST METHODS ####################################

def getWinners(players, game):
    """
    Return a list of winners
    :param players:
    :param game:
    :return:
    """

    # get score for each player
    for i in range(0, len(game.players)):
        game.players[i].credits = scoreFor(i, game)

    currentPlayer = whoseTurn(game)

    # add 1 to players who had less turns
    best = 0
    winners = []
    for i in range(0, len(game.players)):
        if best < game.players[i].credits:
            best = game.players[i].credits
            winners.append(i)
        elif best == game.players[i].credits:
            if i <= currentPlayer:
                winners.append(i)
            else:
                if currentPlayer in winners:
                    winners = []
                winners.append(i)

    return winners


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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.whoseTurn = 0
    game.players[game.whoseTurn].handCards = [enums.Card.chapel, enums.Card.councilroom,
                                             enums.Card.gardens, enums.Card.chancellor,
                                             enums.Card.chapel]

    trashsize = len(game.players[game.whoseTurn].trash)

    playCard(0, 0, 0, 0, game)

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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.whoseTurn = 0
    game.players[game.whoseTurn].handCards = [enums.Card.chapel, enums.Card.councilroom,
                                             enums.Card.gardens, enums.Card.chancellor,
                                             enums.Card.adventurer]

    trashsize = len(game.players[game.whoseTurn].trash)

    playCard(0, 0, 0, 0, game)

    nums = 0
    for i in range(0, len(game.players[game.whoseTurn].handCards)):
        if enums.Card.chapel == game.players[game.whoseTurn].handCards[i]:
            nums += 1

    if 0 == nums and trashsize == len(game.players[game.whoseTurn].trash):
        print "test case 1 for chapel card: Passed!\n"
    else:
        print "test case 2 for chapel card: Failed.\n"


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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

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

    playCard(0, 0, 0, 0, game)

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


def runFeastTestCase1():
    """
    Precondition: there should be at least a feast card in hand.
    Test case description: play the feast card in hand.
    Expected result: The gained card goes into the Discard pile.
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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.whoseTurn = 0
    game.players[game.whoseTurn].handCards = [enums.Card.feast, enums.Card.copper,
                                             enums.Card.copper, enums.Card.chapel,
                                             enums.Card.copper]

    discardcountbefore = game.players[game.whoseTurn].discardCardCount()

    playCard(0, 1, 0, 0, game)

    discardcardcountafter = game.players[game.whoseTurn].discardCardCount()

    if discardcountbefore == discardcardcountafter - 2:
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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

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

    result = playCard(0, 1, 0, 0, game)

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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

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

    result = playCard(0, 3, 0, 0, game)

    if result == -1 and game.error == "That card is too expensive!":
        print "test case 3 for feast card: Passed!\n"
    else:
        print "test case 3 for feast card: Failed.\n"


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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

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

    playCard(0, 0, 0, 0, game)

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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

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


    playCard(0, 0, 0, 0, game)

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


def runCellarTestCase1():
    """
    Precondition: There should be at least a cellar card in hand.
    Test case description: play the cellar card in hand, and discard 2 hand cards.
    Expected result: The number of hand cards = current hand cards - 1; add one more action.
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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.whoseTurn = 0
    game.players[game.whoseTurn].handCards = [enums.Card.cellar, enums.Card.copper,
                                             enums.Card.copper, enums.Card.chapel,
                                             enums.Card.copper]

    handcardbefore = game.players[game.whoseTurn].handCardCount()
    actionsbefore = game.numActions

    playCard(0, 3, -1, -1, game)

    handcardafter = game.players[game.whoseTurn].handCardCount()
    actionsafter = game.numActions

    if handcardbefore == handcardafter + 1 and actionsbefore == actionsafter:
        print "test case 1 for cellar card: Passed!\n"
    else:
        print "test case 1 for cellar card: Failed.\n"


def runChancellorTestCase1():
    """
    Precondition: There should be at least a chancellor card in hand.
    Test case description: play the cellar card in hand, and discard 2 hand cards.
    Expected result: The number of hand cards = current hand cards - 1; add one more action.
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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

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

    playCard(0, -1, -1, -1, game)

    deckafter = game.players[game.whoseTurn].deckCount()
    discardafter = game.players[game.whoseTurn].discardCardCount()
    coinsafter = game.players[game.whoseTurn].coins

    if deckafter == 0 and discardafter == deckbefore + discardbefore + 1 and coinsbefore == coinsafter - 2:
        print "test case 1 for chancellor card: Passed!\n"
    else:
        print "test case 1 for chancellor card: Failed.\n"


def runFestivalTestCase1():
    """
    Precondition: There should be at least a festival card in hand.
    Test case description: play the festival card in hand.
    Expected result: +2 actions, +2 coins, and +1 Buy.
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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.whoseTurn = 0
    game.players[game.whoseTurn].handCards = [enums.Card.festival, enums.Card.bureaucrat,
                                             enums.Card.adventurer, enums.Card.chapel,
                                             enums.Card.cellar]

    actionsbefore = game.numActions
    buysbefore = game.numBuys
    coinsbefore = game.players[game.whoseTurn].coins

    playCard(0, -1, -1, -1, game)

    actionsafter = game.numActions
    buysafter = game.numBuys
    coinsafter = game.players[game.whoseTurn].coins

    if actionsbefore == actionsafter - 1 and buysbefore == buysafter - 1 and coinsbefore == coinsafter - 2:
        print "test case 1 for festival card: Passed!\n"
    else:
        print "test case 1 for festival card: Failed.\n"


def runLaboratoryTestCase1():
    """
    Precondition: There should be at least a laboratory card in hand.
    Test case description: play the laboratory card in hand.
    Expected result: +2 cards in hand and +1 action.
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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.whoseTurn = 0
    game.players[game.whoseTurn].handCards = [enums.Card.laboratory, enums.Card.bureaucrat,
                                             enums.Card.adventurer, enums.Card.chapel,
                                             enums.Card.cellar]

    actionsbefore = game.numActions
    handsizebefore = game.players[game.whoseTurn].handCardCount()

    playCard(0, -1, -1, -1, game)

    actionsafter = game.numActions
    handsizeafter = game.players[game.whoseTurn].handCardCount()

    if actionsbefore == actionsafter - 1 and handsizebefore == handsizeafter - 1:
        print "test case 1 for laboratory card: Passed!\n"
    else:
        print "test case 1 for laboratory card: Failed.\n"


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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

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


    playCard(0, -1, -1, -1, game)


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


def runSmithyTestCase1():
    """
    Precondition: There should be at least a smithy card in hand.
    Test case description: play the smithy card in hand.
    Expected result: your handsize +3.
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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.whoseTurn = 0
    game.players[game.whoseTurn].handCards = [enums.Card.smithy, enums.Card.bureaucrat,
                                             enums.Card.adventurer, enums.Card.chapel,
                                             enums.Card.cellar]

    handsizebefore = game.players[game.whoseTurn].handCardCount()

    playCard(0, -1, -1, -1, game)

    handsizeafter = game.players[game.whoseTurn].handCardCount()

    if handsizebefore == handsizeafter - 2:
        print "test case 1 for smithy card: Passed!\n"
    else:
        print "test case 1 for smithy card: Failed.\n"


def runVillageTestCase1():
    """
    Precondition: There should be at least a village card in hand.
    Test case description: play the village card in hand.
    Expected result: +2 actions and +1 Card.
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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.whoseTurn = 0
    game.players[game.whoseTurn].handCards = [enums.Card.village, enums.Card.bureaucrat,
                                             enums.Card.adventurer, enums.Card.chapel,
                                             enums.Card.cellar]

    actionsbefore = game.numActions
    handsizebefore = game.players[game.whoseTurn].handCardCount()

    playCard(0, -1, -1, -1, game)

    actionsafter = game.numActions
    handsizeafter = game.players[game.whoseTurn].handCardCount()

    if actionsbefore == actionsafter - 1 and handsizebefore == handsizeafter:
        print "test case 1 for village card: Passed!\n"
    else:
        print "test case 1 for village card: Failed.\n"


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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    originalphase = game.phase
    game.phase = enums.GamePhase.buy

    result = playCard(0, -1, -1, -1, game)

    if result == -1 and game.error == "Not allowed to play card in non-action phase.\n":
        print "test case 1 for playCard function: Passed!\n"
    else:
        print "test case 1 for playCard function: Failed.\n"

    game.phase = originalphase
    game.error = ""

    originalactions = game.numActions
    game.numActions = 0

    result = playCard(0, -1, -1, -1, game)

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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.phase = enums.GamePhase.action
    game.whoseTurn = 0
    game.players[game.whoseTurn].handCards = [enums.Card.copper, enums.Card.bureaucrat,
                                             enums.Card.adventurer, enums.Card.chapel,
                                             enums.Card.cellar]

    result = playCard(0, -1, -1, -1, game)

    if result == -1 and game.error == "Play action cards first.":
        print "test case 2 for playCard function when playing non-action cards: Passed!\n"
    else:
        print "test case 2 for playCard function when playing non-action cards: Failed.\n"

    game.error = ""
    game.players[game.whoseTurn].handCards[0] = 20

    result = playCard(0, -1, -1, -1, game)

    if result == -1 and game.error == "This is an invalid card.\n":
        print "test case 2 for playCard function when playing an invalid card: Passed!\n"
    else:
        print "test case 2 for playCard function when playing an invalid card: Failed.\n"


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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    originalcoins = game.players[game.whoseTurn].coins
    game.players[game.whoseTurn].coins = 0

    result = buyCard(enums.Card.province, game)

    if result == -1 and game.error == "You do not have enough money to buy that.\n":
        print "test case 1 for buyCard function without enough coins to buy: Passed!\n"
    else:
        print "test case 1 for buyCard function without enough coins to buy: Failed.\n"

    game.players[game.whoseTurn].coins = originalcoins
    game.error = ""

    provincecount = game.supplies.provinceCount
    game.supplies.provinceCount = 0

    result = buyCard(enums.Card.province, game)

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

    result = buyCard(enums.Card.province, game)

    if result == -1 and game.error == "You do not have any buys left\n":
        print "test case 1 for playCard function with numBuys = 0: Passed!\n"
    else:
        print "test case 1 for playCard function with numBuys = 0: Failed.\n"

    game.numBuys = numbuy
    game.players[game.whoseTurn].coins = coins
    game.error = ""

    current = game.whoseTurn
    result = endTurn(game)
    next = game.whoseTurn

    if result == 0 and next == (current + 1) % len(game.players):
        print "test case 1 for endTurn function: Passed!\n"
    else:
        print "test case 1 for endTurn function: Failed.\n"

    result = isGameOver(game)

    if not result:
        print "test case 1 for isGameOver function: Passed!\n"
    else:
        print "test case 1 for isGameOver function: Failed.\n"

    provinces = game.supplies.provinceCount
    game.supplies.provinceCount = 0

    result = isGameOver(game)
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

    result = isGameOver(game)
    if result:
        print "test case 3 for isGameOver function: Passed!\n"
    else:
        print "test case 3 for isGameOver function: Failed.\n"


def runGetWinnerTestCase1():
    """
    This test case is designed to test getWinner function.
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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.whoseTurn = 0

    winners = getWinners(game.players, game)

    if len(winners) == 1 and winners[0] == 1:
        print "test case 1 for getWinner function: Passed!\n"
    else:
        print "test case 1 for getWinner function: Failed.\n"


def runGetWinnerTestCase2():
    """
    This test case is designed to test getWinner function.
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

    game = initializeGame(numPlayers, kingdomCards, randomSeed)

    if len(game.error) > 0:
        print game.error
        return

    game.whoseTurn = 1

    winners = getWinners(game.players, game)

    if len(winners) == 2:
        print "test case 2 for getWinner function: Passed!\n"
    else:
        print "test case 2 for getWinner function: Failed.\n"



def main(argv):

    runChapelTestCase1()

    runChapelTestCase2()

    runAdventurerTestCase1()

    runFeastTestCase1()

    runFeastTestCase2()

    runFeastTestCase3()

    runCouncilroomTestCase1()

    runBureaucratTestCase1()

    runCellarTestCase1()

    runChancellorTestCase1()

    runFestivalTestCase1()

    runLaboratoryTestCase1()

    runSeahagTestCase1()

    runSmithyTestCase1()

    runVillageTestCase1()

    runPlaycardTestCase1()

    runPlaycardTestCase2()

    runBuycardTestCase1()

    runGetWinnerTestCase1()

    runGetWinnerTestCase2()


if __name__ == "__main__":
    main(sys.argv[1:])
