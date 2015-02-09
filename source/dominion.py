__author__ = 'liux4@onid.oregonstate.edu'

import enums
import rngs

from math import *
import random
import copy

# APIs definition of dominion game


def initializeGame(numPlayers, kingdomCards, randomSeed):

    """
    Initialize a new game with all supplies, and shuffling deck and
    drawing starting hands for all players.  Check that 10 cards selected
    are in fact (different) kingdom cards, and that numPlayers is valid.

    :param numPlayers: the number of players participating the game.
    :param kingdomCards: the kingdom cards.
    :param randomSeed:
    :rtype : int
    """

    # set up random number generator. TODO: refactor this random generator logic
    #rngs.selectStream(1)
    #rngs.putSeed(randomSeed)

    # check the number of players
    if numPlayers > enums.MAX_PLAYERS or numPlayers < 2:
        return -1

    # instantiate an object of GameState and set the number of players
    state = enums.GameState(numPlayers)
    # state.players = numPlayers

    # check selected kingdom cards are different
    if len(kingdomCards) != len(set(kingdomCards)):
        return -1

    # set number of Curse cards
    # 10 Curse cards in the Supply for a 2 player game,
    # 20 Curse cards for 3 players, and
    # 30 Curse cards for 4 players.
    if numPlayers == 2:
        state.supplies.curseCount = 10
    elif numPlayers == 3:
        state.supplies.curseCount = 20
    else:
        state.supplies.curseCount = 30

    # 48 Victory cards
    # After each player takes 3 Estate cards,
    # 3 or 4 player game: 12 Estate, 12 Duchy, and 12 Province cards in the Supply.
    # 2 player game: 8 Estate, 8 Duchy, and 8 Province cards in the Supply.
    if numPlayers == 2:
        state.supplies.estateCount = 8
        state.supplies.duchyCount = 8
        state.supplies.provinceCount = 8
    else:
        state.supplies.estateCount = 12
        state.supplies.duchyCount = 12
        state.supplies.provinceCount = 12

    # set number of Treasure cards
    state.supplies.copperCount = 60
    state.supplies.silverCount = 40
    state.supplies.goldCount = 30

    for i in range(numPlayers):
        state.players[i].gold = 7
        state.supplies.copperCount -= 7

    # set number of Kingdom cards
    for i in range(10):
        if kingdomCards[i] == enums.Card.adventurer:
            state.supplies.adventurerCount = 10
        elif kingdomCards[i] == enums.Card.bureaucrat:
            state.supplies.bureaucratCount = 10
        elif kingdomCards[i] == enums.Card.cellar:
            state.supplies.cellarCount = 10
        elif kingdomCards[i] == enums.Card.chapel:
            state.supplies.chapelCount = 10
        elif kingdomCards[i] == enums.Card.chancellor:
            state.supplies.chancellorCount = 10
        elif kingdomCards[i] == enums.Card.councilroom:
            state.supplies.councilroomCount = 10
        elif kingdomCards[i] == enums.Card.feast:
            state.supplies.feastCount = 10
        elif kingdomCards[i] == enums.Card.festival:
            state.supplies.festivalCount = 10
        elif kingdomCards[i] == enums.Card.gardens:
            state.supplies.gardensCount = 12  # victory cards
        elif kingdomCards[i] == enums.Card.laboratory:
            state.supplies.laboratoryCount = 10
        elif kingdomCards[i] == enums.Card.library:
            state.supplies.libraryCount = 10
        elif kingdomCards[i] == enums.Card.market:
            state.supplies.marketCount = 10
        elif kingdomCards[i] == enums.Card.militia:
            state.supplies.militiaCount = 10
        elif kingdomCards[i] == enums.Card.mine:
            state.supplies.mineCount = 10
        elif kingdomCards[i] == enums.Card.moat:
            state.supplies.moatCount = 10  # action-reaction card
        elif kingdomCards[i] == enums.Card.moneylender:
            state.supplies.moneylenderCount = 10
        elif kingdomCards[i] == enums.Card.remodel:
            state.supplies.remodelCount = 10
        elif kingdomCards[i] == enums.Card.smithy:
            state.supplies.smithyCount = 10
        elif kingdomCards[i] == enums.Card.spy:
            state.supplies.spyCount = 10
        elif kingdomCards[i] == enums.Card.thief:
            state.supplies.thiefCount = 10
        elif kingdomCards[i] == enums.Card.throneroom:
            state.supplies.throneroomCount = 10
        elif kingdomCards[i] == enums.Card.village:
            state.supplies.villageCount = 10
        elif kingdomCards[i] == enums.Card.witch:
            state.supplies.witchCount = 10
        elif kingdomCards[i] == enums.Card.woodcutter:
            state.supplies.woodcutterCount = 10
        elif kingdomCards[i] == enums.Card.workshop:
            state.supplies.workshopCount = 10
        else:
            return None

    # set player decks
    for i in range(0, numPlayers):
        state.deckCount[i] = 0
        state.players[i].cardsInDeck.append
        for j in range(3):
            state.deck[i][j] = enums.Card.estate
            state.deckCount[i] += 1

        for j in range(3, 10):
            state.deck[i][j] = enums.Card.copper
            state.deckCount[i] += 1

    # shuffle player decks
    for i in range(0, numPlayers):
        result = shuffle(i, state)
        assert (result == 0), "Failed to shuffle the deck of player{0:d}.\n".format(i)

    # draw player hands
    for i in range(0, numPlayers):
        # initialize hand size to zero
        state.handCount[i] = 0
        state.discardCount[i] = 0

        # draw 5 cards
        for j in range(5):
            drawCard(i, state)

    # set embargo tokens to 0 for all supply piles
    for i in range(0, int(enums.Card.treasuremap) + 1):
        state.embargoTokens[i] = 0

    # initialize first player's turn
    state.outpostPlayed = 0
    state.phase = 0
    state.numActions = 1
    state.numBuys = 1
    state.playedCardCount = 0
    state.whoseTurn = 0
    state.handCount[state.whoseTurn] = 0

    updateCoins(state.whoseTurn, state, 0)

    return 0


def initialize(numPlayers, kingdomCards, randomseed):

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

    # for i in range(0, numPlayers):
    #     game.players[i].copper = 7
    #     game.supplies.copperCount -= 7

    # # set number of Kingdom cards
    game.supplies.setSupplyKingdoms(kingdomCards)

    # for i in range(0, 10):
    #     if kingdomCards[i] == enums.Card.adventurer:
    #         game.supplies.adventurerCount = 10
    #     elif kingdomCards[i] == enums.Card.bureaucrat:
    #         game.supplies.bureaucratCount = 10
    #     elif kingdomCards[i] == enums.Card.cellar:
    #         game.supplies.cellarCount = 10
    #     elif kingdomCards[i] == enums.Card.chapel:
    #         game.supplies.chapelCount = 10
    #     elif kingdomCards[i] == enums.Card.chancellor:
    #         game.supplies.chancellorCount = 10
    #     elif kingdomCards[i] == enums.Card.councilroom:
    #         game.supplies.councilroomCount = 10
    #     elif kingdomCards[i] == enums.Card.feast:
    #         game.supplies.feastCount = 10
    #     elif kingdomCards[i] == enums.Card.festival:
    #         game.supplies.festivalCount = 10
    #     elif kingdomCards[i] == enums.Card.gardens:
    #         game.supplies.gardensCount = 12  # victory cards
    #     elif kingdomCards[i] == enums.Card.laboratory:
    #         game.supplies.laboratoryCount = 10
    #     elif kingdomCards[i] == enums.Card.library:
    #         game.supplies.libraryCount = 10
    #     elif kingdomCards[i] == enums.Card.market:
    #         game.supplies.marketCount = 10
    #     elif kingdomCards[i] == enums.Card.militia:
    #         game.supplies.militiaCount = 10
    #     elif kingdomCards[i] == enums.Card.mine:
    #         game.supplies.mineCount = 10
    #     elif kingdomCards[i] == enums.Card.moat:
    #         game.supplies.moatCount = 10  # action-reaction card
    #     elif kingdomCards[i] == enums.Card.moneylender:
    #         game.supplies.moneylenderCount = 10
    #     elif kingdomCards[i] == enums.Card.remodel:
    #         game.supplies.remodelCount = 10
    #     elif kingdomCards[i] == enums.Card.smithy:
    #         game.supplies.smithyCount = 10
    #     elif kingdomCards[i] == enums.Card.spy:
    #         game.supplies.spyCount = 10
    #     elif kingdomCards[i] == enums.Card.thief:
    #         game.supplies.thiefCount = 10
    #     elif kingdomCards[i] == enums.Card.throneroom:
    #         game.supplies.throneroomCount = 10
    #     elif kingdomCards[i] == enums.Card.village:
    #         game.supplies.villageCount = 10
    #     elif kingdomCards[i] == enums.Card.witch:
    #         game.supplies.witchCount = 10
    #     elif kingdomCards[i] == enums.Card.woodcutter:
    #         game.supplies.woodcutterCount = 10
    #     elif kingdomCards[i] == enums.Card.workshop:
    #         game.supplies.workshopCount = 10
    #     else:
    #         game.error += 'Undefined kingdom card: {0:s}.\n'.format(str(kingdomCards[i]))
    #         return game

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
            drawCard(i, game)

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
        updateCoins(i, game, 0)

    return game


def shuffle(player, state):
    if state.players[player].deckCount() < 1:
        state.error = "Failed to shuffle the cards on the deck of Player{0:d}. The deck is empty."
        return -1

    try:
        random.shuffle(state.players[player].cardsInDeck)
    except:
        state.error = "Unexpected error: " + sys.exc_info()[0]
        return -1

    return 0


# def qsort(cards):
#
#     if len(cards) > 0:
#         if len(cards) == 1:
#             return cards
#         else:
#             return qsort([x for x in cards[1:] if x < cards[0]]) + \
#                    [cards[0]] + \
#                    qsort([x for x in cards[1:] if x >= cards[0]])


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
    if cardEffect(card, choice1, choice2, choice3, game, handPos, coinbonus) < 0:
        return -1

    # reduce number of actions
    game.numActions -= 1

    # update coins (Treasure cards may be added with card draws)
    updateCoins(game.whoseTurn, game, coinbonus)

    return 0


# TODO: NEED MORE EFFORTS
def buyCard(supplyPos, state):

    assert isinstance(state, enums.GameState)

    print "Entering buyCard...\n"

    who = state.whoseTurn

    if state.numBuys < 1:

        # DEBUG
        print "You do not have any buys left\n"
        return -1

    elif supplyCount(supplyPos, state) < 1:

        # DEBUG
        print "There are not any of that type of card left\n"
        return -1

    elif state.coins < getCost(supplyPos):

        # DEBUG
        print "You do not have enough money to buy that. You have {0:d} coins.\n".format(state.coins)
        return -1

    else:
        state.phase = 1
        result = gainCard(supplyPos, state, 0, who)
        assert (result != -1), "The returned value of gainCard should not be -1."

        # pay for the new card
        state.coins -= getCost(supplyPos)
        state.numBuys -= 1

        # DEBUG
        print "You bought card number {0:d} for {0:d} coins. You now have {0:d} buys and {0:d} coins.\n".format(
            supplyPos, getCost(supplyPos), state.numBuys, state.coins)

    return 0


# Compute how many cards current player has in hand
def numHandCards(state):
    return state.players[state.whoseTurn].handCardCount


def handCard(handPos, state):
    return state.players[state.whoseTurn].handCards[handPos]


def supplyCount(card, state):

    # curse card
    if card == enums.Card.curse:
        return state.supplies.curseCount

    # Victory cards
    if card == enums.Card.estate:
        return state.supplies.estateCount
    elif card == enums.Card.duchy:
        return state.supplies.duchyCount
    elif card == enums.Card.province:
        return state.supplies.provinceCount

    # Treasure cards
    if card == enums.Card.copper:
        return state.supplies.copperCount
    elif card == enums.Card.silver:
        return state.supplies.silverCount
    elif card == enums.Card.gold:
        return state.supplies.goldCount

    # Kingdom cards
    if enums.Card.adventurer <= card <= enums.Card.workshop:
        return state.supplies.kingdoms[card]

    return -1


    # if card == enums.Card.adventurer:
    #     return state.supplies.adventurerCount
    # elif card == enums.Card.adventurer:
    #     return state.supplies.adventurerCount
    # elif card == enums.Card.bureaucrat:
    #     return state.supplies.bureaucratCount
    # elif card == enums.Card.cellar:
    #     return state.supplies.cellarCount
    # elif card == enums.Card.chapel:
    #     return state.supplies.chapelCount
    # elif card == enums.Card.chancellor:
    #     return state.supplies.chancellorCount
    # elif card == enums.Card.councilroom:
    #     return state.supplies.councilroomCount
    # elif card == enums.Card.feast:
    #     return state.supplies.feastCount
    # elif card == enums.Card.festival:
    #     return state.supplies.festivalCount
    # elif card == enums.Card.gardens:
    #     return state.supplies.gardensCount  # victory cards
    # elif card == enums.Card.laboratory:
    #     return state.supplies.laboratoryCount
    # elif card == enums.Card.library:
    #     return state.supplies.libraryCount
    # elif card == enums.Card.market:
    #     return state.supplies.marketCount
    # elif card == enums.Card.militia:
    #     return state.supplies.militiaCount
    # elif card == enums.Card.mine:
    #     return state.supplies.mineCount
    # elif card == enums.Card.moat:
    #     return state.supplies.moatCount  # action-reaction card
    # elif card == enums.Card.moneylender:
    #     return state.supplies.moneylenderCount
    # elif card == enums.Card.remodel:
    #     return state.supplies.remodelCount
    # elif card == enums.Card.smithy:
    #     return state.supplies.smithyCount
    # elif card == enums.Card.spy:
    #     return state.supplies.spyCount
    # elif card == enums.Card.thief:
    #     return state.supplies.thiefCount
    # elif card == enums.Card.throneroom:
    #     return state.supplies.throneroomCount
    # elif card == enums.Card.village:
    #     return state.supplies.villageCount
    # elif card == enums.Card.witch:
    #     return state.supplies.witchCount
    # elif card == enums.Card.woodcutter:
    #     return state.supplies.woodcutterCount
    # elif card == enums.Card.workshop:
    #     return state.supplies.workshopCount
    # else:
    #     return -1


def fullDeckCount(player, card, state):
    """
    Here deck = hand + discard + deck
    :param player:
    :param card:
    :param state:
    :return:
    """

    count = 0

    for i in range(state.players[player].deckCount()):
        if state.players[player].cardsInDeck[i] == card:
            count += 1

    for i in range(state.players[player].handCardCount()):
        if state.players[player].handCards[i] == card:
            count += 1

    for i in range(state.players[player].discardCardCount()):
        if state.players[player].discardCards[i] == card:
            count += 1

    return count


def whoseTurn(state):
    return state.whoseTurn


def endTurn(state):

    currentPlayer = whoseTurn(state)

    # Discard hand
    state.players[currentPlayer].discardCards.append(state.players[currentPlayer].handCards)
    state.players[currentPlayer].handCards = []

    # determine next player
    state.whoseTurn = (currentPlayer + 1) % len(state.players)

    state.outpostPlayed = 0
    state.phase = 0
    state.numActions = 1
    state.coins = 0
    state.numBuys = 1
    state.playedCardCount = 0
    state.players[state.whoseTurn].handCards = []

    # Next player draws 5 handcards
    for k in range(0, 5):
        drawCard(state.whoseTurn, state)

    # Update money
    updateCoins(state.whoseTurn, state, 0)

    return 0


def isGameOver(state):

    # The game ends at the end of any player turn when either
    # 1) the Supply pile of Province cards is empty or
    # 2) any 3 Supply piles are empty.

    if state.supplies.provinceCount == 0:
        return True

    counter = 0

    # curse card
    if state.supplies.curseCount == 0:
        counter += 1

    # Victory cards
    if state.supplies.estateCount == 0:
        counter += 1

    if state.supplies.duchyCount == 0:
        counter += 1

    if state.supplies.provinceCount == 0:
        counter += 1

    # Treasure cards
    if state.supplies.copperCount == 0:
        counter += 1

    if state.supplies.silverCount == 0:
        counter += 1

    if state.supplies.goldCount == 0:
        counter += 1

    for i in range(0, len(state.supplies.kingdoms)):
        if state.supplies.kingdoms[i] == 0:
            counter += 1

    if counter >= 3:
        return True
    else:
        return False


# TODO: need to refactor
def scoreFor(player, state):

    # assert isinstance(state, enums.GameState)
    #
    # score = 0
    #
    # # score from hand
    # for i in range(state.handCount[player]):
    #     if state.hand[player][i] == enums.Card.curse:
    #         score -= 1
    #     elif state.hand[player][i] == enums.Card.estate:
    #         score += 1
    #     elif state.hand[player][i] == enums.Card.duchy:
    #         score += 3
    #     elif state.hand[player][i] == enums.Card.province:
    #         score += 6
    #     elif state.hand[player][i] == enums.Card.greathall:
    #         score += 1
    #     elif state.hand[player][i] == enums.Card.gardens:
    #         score += (fullDeckCount(player, 0, state) / 10)
    #
    # # score from discard
    # for i in range(state.discard[player]):
    #     if state.discard[player][i] == enums.Card.curse:
    #         score -= 1
    #     elif state.discard[player][i] == enums.Card.estate:
    #         score += 1
    #     elif state.discard[player][i] == enums.Card.duchy:
    #         score += 3
    #     elif state.discard[player][i] == enums.Card.province:
    #         score += 6
    #     elif state.discard[player][i] == enums.Card.greathall:
    #         score += 1
    #     elif state.discard[player][i] == enums.Card.gardens:
    #         score += (fullDeckCount(player, 0, state) / 10)
    #
    # # score from deck
    # for i in range(state.deck[player]):
    #     if state.deck[player][i] == enums.Card.curse:
    #         score -= 1
    #     elif state.deck[player][i] == enums.Card.estate:
    #         score += 1
    #     elif state.deck[player][i] == enums.Card.duchy:
    #         score += 3
    #     elif state.deck[player][i] == enums.Card.province:
    #         score += 6
    #     elif state.deck[player][i] == enums.Card.greathall:
    #         score += 1
    #     elif state.deck[player][i] == enums.Card.gardens:
    #         score += (fullDeckCount(player, 0, state) / 10)

    # return score
    return 0


# TODO: CHECK THE RETURN VALUE
def getWinners(players, state):

    assert isinstance(state, enums.GameState)

    # get score for each player
    for i in range(enums.MAX_PLAYERS):
        # set unused player scores to -9999
        if i >= state.numPlayers:
            players[i] = -9999
        else:
            players[i] = scoreFor(i, state)

    # find highest score
    j = 0
    for i in range(enums.MAX_PLAYERS):
        if players[i] > players[j]:
            j = i

    highScore = players[j]

    # add 1 to players who had less turns
    currentPlayer = whoseTurn(state)
    for i in range(enums.MAX_PLAYERS):
        if players[i] == highScore and i > currentPlayer:
            players[i] += 1

    # find new highest score
    j = 0
    for i in range(enums.MAX_PLAYERS):
        if players[i] > players[j]:
            j = i

    highScore = players[j]

    # set winners in array to 1 and rest to 0
    for i in range(enums.MAX_PLAYERS):
        if players[i] == highScore:
            players[i] = 1

        else:
            players[i] = 0

    return 0


# TODO: NEED MORE EFFORTS
def cardEffect(card, choice1, choice2, choice3, state, handPos, bonus):

    currentPlayer = whoseTurn(state)
    nextPlayer = (currentPlayer + 1) % len(state.players)

    tributeRevealedCards = [-1, -1]
    temphand = []  # temphand[MAX_HAND]  # moved above the if statement

    z = 0  # this is the counter for the temp hand

    if card == enums.Card.adventurer:  # 7
        # reveal cards from your deck until you reveal 2 Treasure cards.
        # put those Treasure cards into your hands and discard the other
        # revealed cards.
        drawntreasure = 0
        while drawntreasure < 2:
            if state.players[currentPlayer].deckCount() < 1:
                # if the deck is empty we need to shuffle discard and add to deck
                shuffle(currentPlayer, state)

            drawCard(currentPlayer, state)

            # top card of hand is most recently drawn card.
            cardDrawn = state.players[currentPlayer].handCards[-1]

            if cardDrawn == enums.Card.copper or cardDrawn == enums.Card.silver or cardDrawn == enums.Card.gold:
                drawntreasure += 1
            else:
                state.players[currentPlayer].handCards.pop(-1)
                state.players[currentPlayer].discardCards.append(cardDrawn)

        state.players[state.whoseTurn].handCards.pop(handPos)
        state.players[state.whoseTurn].discardCards.append(card)

        return 0

    elif card == enums.Card.bureaucrat:  # 8
        # Bureaucrat - If you have no cards left in your Deck when you
        # play this card, the Silver you gain will become the only card in
        # your Deck. Similarly, if another player has no cards in his Deck,
        # the Victory card he puts on top will become the only card in his Deck.

        for i in range(0, len(state.players)):
            if i != currentPlayer:
                for j in range(0, state.players[i].handCardCount()):
                    if enums.Card.estate <= state.players[i].handCards[j] <= enums.Card.province:
                        victory = state.players[i].handCards.pop(j)
                        state.players[i].cardsInDeck.insert(0, victory)
                        handPos += 1
                        break

        state.players[currentPlayer].handCards.pop(handPos)
        state.players[currentPlayer].cardsInDeck.append(card)

        state.players[currentPlayer].silver += 1

        return 0

    elif card == enums.Card.cellar:  # 9
        # Cellar - You can't discard Cellar to itself, since it isn't in your
        # hand any longer when you resolve it. You choose what cards to
        # discard and discard them all at once. You only draw cards after
        # you have discarded. If you have to shuffle to do the drawing, the
        # discarded cards will end up shuffled into your new Deck.

        choices = [choice1, choice2, choice3]
        newcards = 0
        for i in range(0, len(choices)):
            if 0 <= choices[i] <= state.players[currentPlayer].handCardCount() - 1 and choices[i] != handPos:
                state.players[currentPlayer].handCards.pop(choices[i])
                if choices[i] < handPos:
                    handPos -= 1

                state.players[currentPlayer].discardCards.append(choices[i])
                newcards += 1

        for i in range(0, newcards):
            drawCard(currentPlayer, state)

        state.players[currentPlayer].handCards.pop(handPos)
        state.players[currentPlayer].discardCards.append(card)
        state.numActions += 1

        return 0

    elif card == enums.Card.chapel:  # 10
        # Chapel - You cannot trash the Chapel itself since it is not in your
        # hand when you resolve it. You could trash a different Chapel card
        # if that card were in your hand.

        for i in range(0, state.players[state.whoseTurn].handCardCount()):
            if handPos != i and enums.Card.chapel == state.players[state.whoseTurn].handCards[i]:
                state.players[state.whoseTurn].trash.append(state.players[state.whoseTurn].handCards.pop(i))
                break

        state.players[currentPlayer].handCards.pop(handPos)
        state.players[currentPlayer].discardCards.append(card)

        return 0

    elif card == enums.Card.chancellor:  # 11
        # Chancellor - You must resolve the Chancellor (decide whether or
        # not to discard your Deck by flipping it into your Discard pile)
        # before doing other things on your turn, like deciding what to
        # buy or playing another Action card. You may not look through
        # your Deck as you discard it.

        state.players[currentPlayer].handCards.pop(handPos)
        state.players[currentPlayer].discardCards.append(card)

        state.players[currentPlayer].coins += 2

        state.players[currentPlayer].discardCards.extend(state.players[currentPlayer].cardsInDeck)
        state.players[currentPlayer].cardsInDeck = []

        return 0

    elif card == enums.Card.councilroom:  # 12
        # Council Room -The other players must draw a card whether
        # they want to or not. All players should shuffle as necessary.

        for i in range(0, len(state.players)):
            if i != currentPlayer:
                drawCard(i, state)

        state.players[currentPlayer].handCards.pop(handPos)
        state.players[currentPlayer].discardCards.append(card)

        return 0

    elif card == enums.Card.feast:  # 13
        # The gained card goes into your Discard pile. It has to be a
        # card from the Supply. You cannot use coins from Treasures or
        # previous Actions (like the Market) to increase the cost of the
        # card that you gain.

        # temphand = copy.deepcopy(state.players[currentPlayer].handCards)
        #
        # state.players[currentPlayer].handCards = []

        coins = state.players[currentPlayer].coins

        # Backup hand
        # Update Coins for Buy
        updateCoins(currentPlayer, state, 5)

        # Buy one card
        count = supplyCount(choice1, state)
        if count <= 0:
            state.error = "None of that card left!"
            return -1

        elif state.players[currentPlayer].coins < getCost(choice1):
            state.error = "That card is too expensive!"
            return -1

        else:
            gainCard(choice1, state, 0, currentPlayer)  # Gain the card and put it into discard cards

        if coins < state.players[currentPlayer].coins:
            state.players[currentPlayer].coins = coins

        state.players[currentPlayer].handCards.pop(handPos)
        state.players[currentPlayer].discardCards.append(card)

        return 0

    elif card == enums.Card.festival:  # 14
        # Festival - it gives both 2 actions, 2 coins, and 1 Buy.

        state.numActions += 2
        state.numBuys += 1
        state.players[currentPlayer].coins += 2

        state.players[currentPlayer].handCards.pop(handPos)
        state.players[currentPlayer].discardCards.append(card)

        return 0

    elif card == enums.Card.gardens:  # 15
        return -1

    elif card == enums.Card.laboratory:  # 16
        # Laboratory - It increases your handsize by giving you +2 cards,
        # and then gives +1 action so you can keep playing more actions.
        state.players[currentPlayer].handCards.pop(handPos)
        state.players[currentPlayer].discardCards.append(card)

        state.numActions += 2

        drawCard(currentPlayer, state)
        drawCard(currentPlayer, state)

        return 0

    elif card == enums.Card.mine:
        j = state.hand[currentPlayer][choice1]  # store card we will trash

        if state.hand[currentPlayer][choice1] < enums.Card.copper or state.hand[currentPlayer][choice1] > enums.Card.gold:
            return -1

        if choice2 > enums.Card.treasuremap or choice2 < enums.Card.curse:
            return -1

        if getCost(state.hand[currentPlayer][choice1]) + 3 > getCost(choice2):
            return -1

        result = gainCard(choice2, state, 2, currentPlayer)
        assert (result != -1), "The returned value of gainCard should not be -1."

        # discard card from hand
        discardCard(handPos, currentPlayer, state, 0)

        # discard trashed card
        for i in range(state.handCount[currentPlayer]):
            if state.hand[currentPlayer][i] == j:
                discardCard(i, currentPlayer, state, 0)
                break

        return 0

    elif card == enums.Card.remodel:

        # TODO:

        return 0

    elif card == enums.Card.smithy:

        # +3 Cards
        for i in range(3):
            drawCard(currentPlayer, state)

        # discard card from hand
        discardCard(handPos, currentPlayer, state, 0)

        return 0

    elif card == enums.Card.village:

        # +1 Card
        drawCard(currentPlayer, state)

        # +2 Actions
        state.numActions += 2

        # discard played card from hand
        discardCard(handPos, currentPlayer, state, 0)

        return 0

    elif card == enums.Card.baron:

        state.numBuys += 1  # Increase buys by 1!

        if choice1 > 0:  # Boolean true or going to discard an estate
            p = 0  # Iterator for hand!
            card_not_discarded = 1  # Flag for discard set!

            while card_not_discarded:

                if state.hand[currentPlayer][p] == enums.Card.estate:  # Found an estate card!
                    state.coins += 4  # Add 4 coins to the amount of coins
                    state.discard[currentPlayer][state.discardCount[currentPlayer]] = state.hand[currentPlayer][p]
                    state.discardCount[currentPlayer] += 1

                    for p in range(state.handCount[currentPlayer]):
                        state.hand[currentPlayer][p] = state.hand[currentPlayer][p+1]

                    state.hand[currentPlayer][state.handCount[currentPlayer]] = -1
                    state.handCount[currentPlayer] -= 1
                    card_not_discarded = 0  # Exit the loop

                elif p > state.handCount[currentPlayer]:

                    # DEBUG
                    print "No estate cards in your hand, invalid choice\n"
                    print "Must gain an estate if there are any\n"

                    if supplyCount(enums.Card.estate, state) > 0:
                        result = gainCard(enums.Card.estate, state, 0, currentPlayer)
                        assert (result != -1), "The returned value of gainCard should not be -1."

                        state.supplies[enums.Card.estate] -= 1  # Decrement estates

                        if supplyCount(enums.Card.estate, state) == 0:
                            isGameOver(state)

                    card_not_discarded = 0  # Exit the loop

                else:
                    p += 1  # Next card

        else:
            if supplyCount(enums.Card.estate, state) > 0:
                result = gainCard(enums.Card.estate, state, 0, currentPlayer)  # Gain an estate
                assert (result != -1), "The returned value of gainCard should not be -1."

                state.supplies[enums.Card.estate] -= 1  # Decrement Estates

                if supplyCount(enums.Card.estate, state) == 0:
                    isGameOver(state)

        return 0

    elif card == enums.Card.greathall:
        # +1 Card
        drawCard(currentPlayer, state)

        # +1 Actions
        state.numActions += 1

        # discard card from hand
        discardCard(handPos, currentPlayer, state, 0)

        return 0

    elif card == enums.Card.minion:

        # +1 action
        state.numActions += 1

        # discard card from hand
        discardCard(handPos, currentPlayer, state, 0)

        if choice1:  # +2 coins
            state.coins += 2

        elif choice2:  # discard hand, redraw 4, other players with 5+ cards discard hand and draw 4
            # discard hand
            while numHandCards(state) > 0:
                discardCard(handPos, currentPlayer, state, 0)

                # draw 4
                for i in range(4):
                    drawCard(currentPlayer, state)

                # other players discard hand and redraw if hand size > 4
                for i in range(0, state.numPlayers):
                    if i != currentPlayer:
                        if state.handCount[i] > 4:
                            # discard hand
                            while state.handCount[i] > 0:
                                discardCard(handPos, i, state, 0)

                            # draw 4
                            for j in range(4):
                                drawCard(i, state)

        return 0

    elif card == enums.Card.steward:

        if choice1 == 1:
            # +2 cards
            drawCard(currentPlayer, state)
            drawCard(currentPlayer, state)
        elif choice1 == 2:
            # +2 coins
            state.coins += 2
        else:
            # trash 2 cards in hand
            discardCard(choice2, currentPlayer, state, 1)
            discardCard(choice3, currentPlayer, state, 1)

        # discard card from hand
        discardCard(handPos, currentPlayer, state, 0)

        return 0

    elif card == enums.Card.tribute:

        if state.discardCount[nextPlayer] + state.deckCount[nextPlayer] <= 1:
            if state.deckCount[nextPlayer] > 0:
                tributeRevealedCards[0] = state.deck[nextPlayer][state.deckCount[nextPlayer]-1]
                state.deckCount[nextPlayer] -= 1

            elif state.discardCount[nextPlayer] > 0:
                tributeRevealedCards[0] = state.discard[nextPlayer][state.discardCount[nextPlayer]-1]
                state.discardCount[nextPlayer] -= 1

            else:
                # No Card to Reveal
                # DEBUG
                print "No cards to reveal\n"

        else:
            if state.deckCount[nextPlayer] == 0:
                for i in range(0, state.discardCount[nextPlayer]):
                    state.deck[nextPlayer][i] = state.discard[nextPlayer][i]  # Move to deck
                    state.deckCount[nextPlayer] += 1
                    state.discard[nextPlayer][i] = -1
                    state.discardCount[nextPlayer] -= 1

                shuffle(nextPlayer, state)  # Shuffle the deck

            tributeRevealedCards[0] = state.deck[nextPlayer][state.deckCount[nextPlayer]-1]
            state.deckCount[nextPlayer] -= 1
            state.deck[nextPlayer][state.deckCount[nextPlayer]] = -1
            state.deckCount[nextPlayer] -= 1
            tributeRevealedCards[1] = state.deck[nextPlayer][state.deckCount[nextPlayer]-1]
            state.deckCount[nextPlayer] -= 1
            state.deck[nextPlayer][state.deckCount[nextPlayer]] = -1
            state.deckCount[nextPlayer] -= 1

            # If we have a duplicate card, just drop one
            if tributeRevealedCards[0] == tributeRevealedCards[1]:
                state.playedCards[state.playedCardCount] = tributeRevealedCards[1]
                state.playedCardCount += 1
                tributeRevealedCards[1] = -1

            for i in range(0, 2):
                if tributeRevealedCards[i] == enums.Card.copper or tributeRevealedCards[i] == enums.Card.silver or tributeRevealedCards[i] == enums.Card.gold:
                    # Treasure cards
                    state.coins += 2

                elif tributeRevealedCards[i] == enums.Card.estate or tributeRevealedCards[i] == enums.Card.duchy or tributeRevealedCards[i] == enums.Card.province or tributeRevealedCards[i] == enums.Card.gardens or tributeRevealedCards[i] == enums.Card.great_hall:
                    drawCard(currentPlayer, state)
                    drawCard(currentPlayer, state)

                else:  # Action Card
                    state.numActions += 2

            return 0

    elif card == enums.Card.ambassador:

        j = 0  # used to check if player has enough cards to discard

        if choice2 > 2 or choice2 < 0:
            return -1

        if choice1 == handPos:
            return -1

        for i in range(0, state.handCount[currentPlayer]):
            if i != handPos and i == state.hand[currentPlayer][choice1] and i != choice1:
                j += 1

        if j < choice2:
            return -1

        # DEBUG
        print "Player {0:d} reveals card number: {1:d}\n".format(currentPlayer, state.hand[currentPlayer][choice1])

        # increase supply count for choosen card by amount being discarded
        state.supplies[state.hand[currentPlayer][choice1]] += choice2

        # each other player gains a copy of revealed card
        for i in range(0, state.numPlayers):
            if i != currentPlayer:
                result = gainCard(state.hand[currentPlayer][choice1], state, 0, i)
                assert (result != -1), "The returned value of gainCard should not be -1."

        # discard played card from hand
        discardCard(handPos, currentPlayer, state, 0)

        # trash copies of cards returned to supply
        for j in range(0, choice2):
            for i in range(0, state.handCount[currentPlayer]):
                if state.hand[currentPlayer][i] == state.hand[currentPlayer][choice1]:
                    discardCard(i, currentPlayer, state, 1)
                    break

        return 0

    elif card == enums.Card.cutpurse:
        updateCoins(currentPlayer, state, 2)

        for i in range(0, state.numPlayers):
            if i != currentPlayer:
                for j in range(0, state.handCount[i]):
                    if state.hand[i][j] == enums.Card.copper:
                        discardCard(j, i, state, 0)
                        break

                    if j == state.handCount[i]:
                        for k in range(0, state.handCount[i]):
                            print "Player {0:d} reveals card number {1:d}\n".format(i, state.hand[i][k])
                        break

        # discard played card from hand
        discardCard(handPos, currentPlayer, state, 0)

        return 0

    elif card == enums.Card.embargo:

        # +2 Coins
        state.coins += 2

        # see if selected pile is in play
        if state.supplies[choice1] == -1:
            return -1

        # add embargo token to selected supply pile
        state.embargoTokens[choice1] += 1

        # trash card
        discardCard(handPos, currentPlayer, state, 1)
        return 0

    elif card == enums.Card.outpost:

        # set outpost flag
        state.outpostPlayed += 1

        # discard card
        discardCard(handPos, currentPlayer, state, 0)
        return 0

    elif card == enums.Card.salvanger:

        # +1 buy
        state.numBuys += 1

        if choice1:
            # gain coins equal to trashed card
            state.coins += getCost(handCard(choice1, state))
            # trash card
            discardCard(choice1, currentPlayer, state, 1)

        # discard card
        discardCard(handPos, currentPlayer, state, 0)
        return 0

    elif card == enums.Card.seahag:

        for i in range(0, state.numPlayers):
            if i != currentPlayer:
                state.deckCount[i] -= 1
                state.discard[i][state.discardCount[i]] = state.deck[i][state.deckCount[i]]
                state.deckCount[i] -= 1
                state.discardCount[i] += 1
                state.deckCount[i] -= 1
                state.deck[i][state.deckCount[i]] = enums.Card.curse  # Top card now a curse

        return 0

    elif card == enums.Card.treasuremap:

        # search hand for another treasure_map
        index = -1
        for i in range(0, state.handCount[currentPlayer]):
            if state.hand[currentPlayer][i] == enums.Card.treasuremap and i != handPos:
                index = i
                break

        if index > -1:
            # trash both treasure cards
            discardCard(handPos, currentPlayer, state, 1);
            discardCard(index, currentPlayer, state, 1);

            # gain 4 Gold cards
            for i in range(0, 4):
                result = gainCard(enums.Card.gold, state, 1, currentPlayer)
                assert (result != -1), "The returned value of gainCard should not be -1."

            # return success
            return 1

        # no second treasure_map found in hand
        return -1

    else:
        return -1


def gainCard(card, state, toFlag, player):

    # Note: card is enum of chosen card

    # check if supply pile is empty (0) or card is not used in game (-1)
    if supplyCount(card, state) < 1:
        return -1

    # added card for [whoseTurn] current player:
    # toFlag = 0 : add to discard
    # toFlag = 1 : add to deck
    # toFlag = 2 : add to hand

    if toFlag == 0:
        state.players[player].discardCards.append(card)
        # state.discard[player][state.discardCount[player]] = card
        # state.discardCount[player] += 1

    elif toFlag == 1:
        state.players[player].cardsInDeck.append(card)

        # state.deck[player][state.deckCount[player]] = card
        # state.deckCount[player] += 1

    elif toFlag == 2:
        state.players[player].handCards.append(card)

        # state.hand[player][state.handCount[player]] = card
        # state.handCount[player] += 1

    else:
        return -1

    # decrease number in supply pile
    if state.supplies.updateSupplyCount(card, 1) == -1:
        state.error = "Failed to update the count of card: {0:d}.".format(card)
        return -1

    return 0


def discardCard(handPos, currentPlayer, state, trashFlag):

    assert isinstance(state, enums.GameState)

    # if card is not trashed, added to Played pile
    if trashFlag == 0:
        # add card to played pile
        state.playedCards[state.playedCardCount] = state.hand[currentPlayer][handPos]
        state.playedCardCount += 1

    elif trashFlag == 2:
      state.discard[currentPlayer][state.discardCount[currentPlayer]] = state.hand[currentPlayer][handPos]
      state.discardCount[currentPlayer] += 1

    return fixCardHole(handPos, currentPlayer, state)


def fixCardHole(handPos, player, state):
    # Assumptions:  player's hand has a -1 at handPos; this must not stand!
    # player's handCount is too high by 1
    # Post:  last card in hand will fill the hole -- we're not shifting down
    if state.handCount[player] != 1:
        state.hand[player][handPos] = state.hand[player][state.handCount[player]-1]

    state.handCount[player] -= 1
    return 0


def updateCoins(player, state, bonus):

    for i in range(0, state.players[player].handCardCount()):
        if state.players[player].handCards[i] == enums.Card.copper:
            state.players[player].coins += 1
        elif state.players[player].handCards[i] == enums.Card.silver:
            state.players[player].coins += 2
        elif state.players[player].handCards[i] == enums.Card.gold:
            state.players[player].coins += 3

    # add bonus
    state.players[player].coins += bonus

    return 0


# NON-API functions

# TODO: CHECK THE RETURN VALUE
def drawCard(player, state):

    if state.players[player].deckCount() <= 0:  # Deck is empty

        # Step 1 Shuffle the discard pile back into a deck

        # Move discard to deck
        state.players[player].cardsInDeck.append(state.players[player].discardCards)
        state.players[player].discardCards = []
        # for i in range(state.players[player].discardCardCount):
        #     state.players[player].cardsInDeck.append(state.players[player].discardCards)
        #     state.deck[player][i] = state.discard[player][i]
        #     state.discard[player][i] = -1

        state.deckCount[player] = state.discardCount[player]
        state.discardCount[player] = 0  # Reset discard

        # Shuffle the deck
        shuffle(player, state)  # Shuffle the deck up and make it so that we can draw

        # Debug statements
        print "Deck count now: {0:d}\n".format(state.deckCount[player])

        state.discardCount[player] = 0

        # Step 2 Draw Card
        count = state.handCount[player]  # Get current player's hand count

        # Debug statements
        print "Current hand count: {0:d}\n".format(count)

        deckCounter = state.deckCount[player]  # Create a holder for the deck count

        if deckCounter == 0:
            return -1

        state.hand[player][count] = state.deck[player][deckCounter - 1]  # Add card to hand
        state.deckCount[player] -= 1
        state.handCount[player] += 1  # Increment hand count

    else:
        # count = state.players[player].handCardCount()  # Get current hand count for player
        # deckCounter = state.players[player].deckCount()  # Create holder for the deck count

        card = state.players[player].cardsInDeck.pop(0)
        state.players[player].handCards.append(card)

        # state.hand[player][count] = state.deck[player][deckCounter - 1]  # Add card to the hand
        # state.deckCount[player] -= 1
        # state.handCount[player] += 1  # Increment hand count

    return 0


def getCost(card):

    if card == enums.Card.curse:
        return 0
    elif card == enums.Card.estate:
        return 2
    elif card == enums.Card.duchy:
        return 5
    elif card == enums.Card.province:
        return 8
    elif card == enums.Card.copper:
        return 0
    elif card == enums.Card.silver:
        return 3
    elif card == enums.Card.gold:
        return 6
    elif card == enums.Card.adventurer:
        return 6
    elif card == enums.Card.councilroom:
        return 5
    elif card == enums.Card.feast:
        return 4
    elif card == enums.Card.gardens:
        return 4
    elif card == enums.Card.mine:
        return 5
    elif card == enums.Card.remodel:
        return 4
    elif card == enums.Card.smithy:
        return 4
    elif card == enums.Card.village:
        return 3
    elif card == enums.Card.baron:
        return 4
    elif card == enums.Card.greathall:
        return 3
    elif card == enums.Card.minion:
        return 5
    elif card == enums.Card.steward:
        return 3
    elif card == enums.Card.tribute:
        return 5
    elif card == enums.Card.ambassador:
        return 3
    elif card == enums.Card.cutpurse:
        return 4
    elif card == enums.Card.embargo:
        return 2
    elif card == enums.Card.outpost:
        return 5
    elif card == enums.Card.salvanger:
        return 4
    elif card == enums.Card.seahag:
        return 4
    elif card == enums.Card.treasuremap:
        return 4
    else:
        return -1