__author__ = 'liux4@onid.oregonstate.edu'

import enums

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
        return -1

    # check if player has enough actions
    if game.numActions < 1:
        return -1

    # get card played
    card = handCard(handPos, game)

    # check if selected card is an action
    # if card < enums.Card.adventurer or card > enums.Card.treasuremap:
    #     return -1

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
        print "You do not have any buys left\n"
        return -1

    elif supplyCount(supplyPos, game) < 1:
        print "There are not any of that type of card left\n"
        return -1

    elif game.players[game.whoseTurn].coins < helper.getCost(supplyPos):
        print "You do not have enough money to buy that. You have {0:d} coins.\n".format(game.players[game.whoseTurn])
        return -1

    else:
        game.phase = 1
        result = helper.gainCard(supplyPos, game, 0, who)

        if result != 0:
            return result

        # pay for the new card
        game.players[game.whoseTurn] -= helper.getCost(supplyPos)
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
        if game.hand[player][i] == enums.Card.curse:
            score -= 1
        elif game.hand[player][i] == enums.Card.estate:
            score += 1
        elif game.hand[player][i] == enums.Card.duchy:
            score += 3
        elif game.hand[player][i] == enums.Card.province:
            score += 6
        elif game.hand[player][i] == enums.Card.gardens:
            score += (fullDeckCount(player, 0, game) / 10)

    return score


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


