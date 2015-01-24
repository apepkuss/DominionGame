__author__ = 'liux4@onid.oregonstate.edu'

import enums

# APIs definition of dominion game

def initializeGame(numPlayers, kingdomCards, randomSeed):

    """

    :rtype : int
    """
    return 0  # TODO: replace with a meaningful game state value.


def isGameOver(gameState):

    # TODO: add concrete logic

    return False


def numHandCards(index, gameState):

    # TODO: add concrete logic

    return 0


def handCard(index, gameState):

    # TODO: add concrete logic

    return enums.Card.curse


def whoseTurn(gameState):
    assert isinstance(gameState.whoseTurn, enums.GameState)
    return gameState.whoseTurn


def playCard(handPos, choice1, choice2, choice3, gameState):

    assert isinstance(gameState, enums.GameState)

    #  check if it is the right phase
    if gameState.phase != 0:
        return -1

    # check if player has enough actions
    if gameState.numActions < 1:
        return -1

    # get card played
    card = handCard(handPos, gameState)

    # check if selected card is an action
    if card < enums.Card.adventurer or card > enums.Card.treasuremap:
        return -1

    # play card
    coinbonus = 0  # tracks coins gain from actions
    if cardEffect(card, choice1, choice2, choice3, gameState, handPos, coinbonus) < 0:
        return -1

    # reduce number of actions
    gameState.numActions

    # update coins (Treasure cards may be added with card draws)
    updateCoins(gameState.whoseTurn, gameState, coinbonus)

    return 0


def cardEffect(card, choice1, choice2, choice3, gameState, handPos, bonus):

    assert isinstance(gameState, enums.GameState)

    # TODO: add concrete code

    return 0


def updateCoins(player, gameState, bonus):

    assert isinstance(gameState, enums.GameState)

    # reset coin count
    gameState.coins = 0

    for i in range(gameState.handCout[player]):
        if gameState.hand[player][i] == enums.Card.copper:
            gameState.coins += 1
        elif gameState.hand[player][i] == enums.Card.silver:
            gameState.coins += 2
        elif gameState.hand[player][i] == enums.Card.gold:
            gameState.coins += 3

    # add bonus
    gameState.coins += bonus

    return 0


def scoreFor (player, gameState):

    assert isinstance(gameState, enums.GameState)

    score = 0

    # score from hand
    for i in range(gameState.handCount[player]):
        if gameState.hand[player][i] == enums.Card.curse:
            score -= 1
        elif gameState.hand[player][i] == enums.Card.estate:
            score += 1
        elif gameState.hand[player][i] == enums.Card.duchy:
            score += 3
        elif gameState.hand[player][i] == enums.Card.province:
            score += 6
        elif gameState.hand[player][i] == enums.Card.great_hall:
            score += 1
        elif gameState.hand[player][i] == enums.Card.gardens:
            score += (fullDeckCount(player, 0, gameState) / 10)

    # score from discard
    for i in range(gameState.discard[player]):
        if gameState.discard[player][i] == enums.Card.curse:
            score -= 1
        elif gameState.discard[player][i] == enums.Card.estate:
            score += 1
        elif gameState.discard[player][i] == enums.Card.duchy:
            score += 3
        elif gameState.discard[player][i] == enums.Card.province:
            score += 6
        elif gameState.discard[player][i] == enums.Card.great_hall:
            score += 1
        elif gameState.discard[player][i] == enums.Card.gardens:
            score += (fullDeckCount(player, 0, gameState) / 10)

    # score from deck
    for i in range(gameState.deck[player]):
        if gameState.deck[player][i] == enums.Card.curse:
            score -= 1
        elif gameState.deck[player][i] == enums.Card.estate:
            score += 1
        elif gameState.deck[player][i] == enums.Card.duchy:
            score += 3
        elif gameState.deck[player][i] == enums.Card.province:
            score += 6
        elif gameState.deck[player][i] == enums.Card.great_hall:
            score += 1
        elif gameState.deck[player][i] == enums.Card.gardens:
            score += (fullDeckCount(player, 0, gameState) / 10)

    return score


def fullDeckCount(player, card, gameState):

    assert isinstance(gameState, enums.GameState)

    count = 0

    for i in range(gameState.deckCount[player]):
        if gameState.deck[player][i] == card:
            count += 1

    for i in range(gameState.handCount[player]):
        if gameState.hand[player][i] == card:
            count += 1

    for i in range(gameState.discardCount[player]):
        if gameState.discard[player][i] == card:
            count += 1

    return count


def buyCard(supplyPos, gameState):

    assert isinstance(gameState, enums.GameState)

    # TODO: add concrete logic

    return 0


def endTurn(gameState):

    assert isinstance(gameState, enums.GameState)

    # TODO: add concrete logic

    return 0
