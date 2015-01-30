__author__ = 'liux4@onid.oregonstate.edu'

import enums
import rngs

from math import *
from array import *

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

    # set up random number generator
    rngs.selectStream(1)
    rngs.putSeed(randomSeed)

    # check number of players
    if numPlayers > enums.MAX_PLAYERS or numPlayers < 2:
        return -1  # TODO: replace 0 with a meaningful game state value.

    state = enums.GameState()
    # set number of players
    state.players = numPlayers  # having problems here

    # check selected kingdom cards are different
    for i in range(10):
        for j in range(10):
            if j != i and kingdomCards[j] == kingdomCards[i]:
                return -1  # TODO: replace 0 with a meaningful game state value.

    # initialize supply

    # set number of Curse cards
    if numPlayers == 2:
        state.supplyCount[enums.Card.curse] = 10
    elif numPlayers == 3:
        state.supplyCount[enums.Card.curse] = 20
    else:
        state.supplyCount[enums.Card.curse] = 30

    # set number of Victory cards
    if numPlayers == 2:
        state.supplyCount[enums.Card.estate] = 8
        state.supplyCount[enums.Card.duchy] = 8
        state.supplyCount[enums.Card.province] = 8
    else:
        state.supplyCount[enums.Card.estate] = 12
        state.supplyCount[enums.Card.duchy] = 12
        state.supplyCount[enums.Card.province] = 12

    # set number of Treasure cards
    state.supplyCount[enums.Card.copper] = 60 - (7 * numPlayers)
    state.supplyCount[enums.Card.silver] = 40
    state.supplyCount[enums.Card.gold] = 30

    # set number of Kingdom cards
    for i in range(int(enums.Card.adventurer), int(enums.Card.treasuremap) + 1):  # loop all cards
        for j in range(10):  # loop chosen cards
            if kingdomCards[j] == i:
                # check if card is a 'Victory' Kingdom card
                if kingdomCards[j] == enums.Card.greathall or kingdomCards[j] == enums.Card.gardens:
                    if numPlayers == 2:
                        state.supplyCount[i] = 8
                    else:
                        state.supplyCount[i] = 12
                else:
                    state.supplyCount[i] = 10

                break
            else:  # card is not in the set chosen for the game
                state.supplyCount[i] = -1

    # supply initialization complete

    # set player decks
    for i in range(numPlayers):

        state.deckCount[i] = 0
        for j in range(3):
            state.deck[i][j] = enums.Card.estate
            state.deckCount[i] += 1

        for j in range(3, 10):
            state.deck[i][j] = enums.Card.copper
            state.deckCount[i] += 1

    # shuffle player decks
    for i in range(numPlayers):
        if shuffle(i, state) < 0:
            return -1  # TODO: replace -1 with a meaningful game state value.

    # draw player hands
    for i in range(numPlayers):
        # initialize hand size to zero
        state.handCount[i] = 0
        state.discardCount[i] = 0

        # draw 5 cards
        for j in range(5):
            drawCard(i, state)

    # set embargo tokens to 0 for all supply piles
    for i in range(int(enums.Card.treasuremap) + 1):
        state.embargoTokens[i] = 0

    # initialize first player's turn
    state.outpostPlayed = 0
    state.phase = 0
    state.numActions = 1
    state.numBuys = 1
    state.playedCardCount = 0
    state.whoseTurn = 0
    state.handCount[state.whoseTurn] = 0
    # int it; move to top

    # Moved draw cards to here, only drawing at the start of a turn
    for i in range(5):
        drawCard(state.whoseTurn, state)

    updateCoins(state.whoseTurn, state, 0)

    return 0  # TODO: replace 0 with a meaningful game state value.


# TODO: NEED MORE EFFORTS
def shuffle(player, state):

    assert isinstance(state, enums.GameState)

    newDeck = []
    newDeckPos = 0

    if state.deckCount[player] < 1:
        return -1

    # TODO: refactor qsort
    # qsort(state.deck[player], state.deckCount[player], sizeof(int), compare)
    qsort(state.deck[player])

    # SORT CARDS IN DECK TO ENSURE DETERMINISM!
    while state.deckCount[player] > 0:
        card = math.floor(random() * state.deckCount[player])  # TODO: refactor
        newDeck[newDeckPos] = state.deck[player][card]
        newDeckPos += 1

        for i in range(card, state.deckCount[player]-1):
            state.deck[player][i] = state.deck[player][i+1]
        state.deckCount[player] -= 1

    for i in range(newDeckPos):
        state.deck[player][i] = newDeck[i]
        state.deckCount[player] += 1

    return 0


def random():

    """
    Random returns a pseudo-random real number uniformly distributed between 0.0 and 1.0.

    :return:
    """

    STREAMS = 256
    MODULUS = 2147483647
    MULTIPLIER = 48271
    DEFAULT = 123456789

    seed = array('l', [DEFAULT])
    stream = 0

    Q = MODULUS / MULTIPLIER
    R = MODULUS % MULTIPLIER
    t = MULTIPLIER * (seed[stream] % Q) - R * (seed[stream] / Q)

    if t > 0:
        seed[stream] = t
    else:
        seed[stream] = t + MODULUS

    return seed[stream] / MODULUS


def qsort(cards):

    if len(cards) > 0:
        if len(cards) == 1:
            return cards
        else:
            return qsort([x for x in cards[1:] if x < cards[0]]) + \
                   [cards[0]] + \
                   qsort([x for x in cards[1:] if x >= cards[0]])


# TODO: CHECK THE RETURN VALUE
def playCard(handPos, choice1, choice2, choice3, state):

    assert isinstance(state, enums.GameState)

    #  check if it is the right phase
    if state.phase != 0:
        return -1

    # check if player has enough actions
    if state.numActions < 1:
        return -1

    # get card played
    card = handCard(handPos, state)

    # check if selected card is an action
    if card < enums.Card.adventurer or card > enums.Card.treasuremap:
        return -1

    # play card
    coinbonus = 0  # tracks coins gain from actions
    if cardEffect(card, choice1, choice2, choice3, state, handPos, coinbonus) < 0:
        return -1

    # reduce number of actions
    state.numActions

    # update coins (Treasure cards may be added with card draws)
    updateCoins(state.whoseTurn, state, coinbonus)

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

    return state.handCount[whoseTurn(state)]


def handCard(handPos, state):

    currentPlayer = whoseTurn(state)
    return state.hand[currentPlayer][handPos]


def supplyCount(card, state):

    assert isinstance(state, enums.GameState)

    return state.supplyCount[card]


def fullDeckCount(player, card, state):

    assert isinstance(state, enums.GameState)

    count = 0

    for i in range(state.deckCount[player]):
        if state.deck[player][i] == card:
            count += 1

    for i in range(state.handCount[player]):
        if state.hand[player][i] == card:
            count += 1

    for i in range(state.discardCount[player]):
        if state.discard[player][i] == card:
            count += 1

    return count


def whoseTurn(state):

    assert isinstance(state, enums.GameState)
    assert isinstance(state.whoseTurn, enums.GameState)
    return state.whoseTurn


# TODO: CHECK THE RETURN VALUE
def endTurn(state):

    assert isinstance(state, enums.GameState)

    currentPlayer = whoseTurn(state)

    # Discard hand
    for i in range(state.handCount[currentPlayer]):
        state.discardCount[currentPlayer] += 1
        state.discard[currentPlayer][state.discardCount[currentPlayer]] = state.hand[currentPlayer][i]
        state.hand[currentPlayer][i] = -1  # Set card to -1

    state.handCount[currentPlayer] = 0  # Reset hand count

    # Code for determining the player
    if currentPlayer < (state.players - 1):
        state.whoseTurn = currentPlayer + 1  # Still safe to increment
    else:
        state.whoseTurn = 0  # Max player has been reached, loop back around to player 1

    state.outpostPlayed = 0
    state.phase = 0
    state.numActions = 1
    state.coins = 0
    state.numBuys = 1
    state.playedCardCount = 0
    state.handCount[state.whoseTurn] = 0

    # int k; move to top
    # Next player draws hand
    for k in range(5):
        drawCard(state.whoseTurn, state)  # Draw a card

    # Update money
    updateCoins(state.whoseTurn, state, 0)

    return 0


def isGameOver(state):

    # TODO: add concrete logic

    # if stack of Province cards is empty, the game ends
    if state.supplyCount[enums.Card.province] == 0:
        return True

    # if three supply pile are at 0, the game ends
    j = 0
    for i in range(25):
        if state.supplyCount[i] == 0:
            j += 1

    if j >= 3:
        return True

    return False


def scoreFor(player, state):

    assert isinstance(state, enums.GameState)

    score = 0

    # score from hand
    for i in range(state.handCount[player]):
        if state.hand[player][i] == enums.Card.curse:
            score -= 1
        elif state.hand[player][i] == enums.Card.estate:
            score += 1
        elif state.hand[player][i] == enums.Card.duchy:
            score += 3
        elif state.hand[player][i] == enums.Card.province:
            score += 6
        elif state.hand[player][i] == enums.Card.greathall:
            score += 1
        elif state.hand[player][i] == enums.Card.gardens:
            score += (fullDeckCount(player, 0, state) / 10)

    # score from discard
    for i in range(state.discard[player]):
        if state.discard[player][i] == enums.Card.curse:
            score -= 1
        elif state.discard[player][i] == enums.Card.estate:
            score += 1
        elif state.discard[player][i] == enums.Card.duchy:
            score += 3
        elif state.discard[player][i] == enums.Card.province:
            score += 6
        elif state.discard[player][i] == enums.Card.greathall:
            score += 1
        elif state.discard[player][i] == enums.Card.gardens:
            score += (fullDeckCount(player, 0, state) / 10)

    # score from deck
    for i in range(state.deck[player]):
        if state.deck[player][i] == enums.Card.curse:
            score -= 1
        elif state.deck[player][i] == enums.Card.estate:
            score += 1
        elif state.deck[player][i] == enums.Card.duchy:
            score += 3
        elif state.deck[player][i] == enums.Card.province:
            score += 6
        elif state.deck[player][i] == enums.Card.greathall:
            score += 1
        elif state.deck[player][i] == enums.Card.gardens:
            score += (fullDeckCount(player, 0, state) / 10)

    return score


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

    assert isinstance(state, enums.GameState)

    currentPlayer = whoseTurn(state)
    nextPlayer = currentPlayer + 1

    tributeRevealedCards = [-1, -1]
    temphand = []  # temphand[MAX_HAND]  # moved above the if statement
    drawntreasure = 0
    z = 0  # this is the counter for the temp hand
    if nextPlayer > (state.numPlayers - 1):
        nextPlayer = 0

    if card == enums.Card.adventurer:
        while drawntreasure < 2:
            if state.deckCount[currentPlayer] < 1:
                # if the deck is empty we need to shuffle discard and add to deck
                shuffle(currentPlayer, state)

                drawCard(currentPlayer, state)
                # top card of hand is most recently drawn card.
                cardDrawn = state.hand[currentPlayer][state.handCount[currentPlayer]-1]

                if cardDrawn == enums.Card.copper or cardDrawn == enums.Card.silver or cardDrawn == enums.Card.gold:
                    drawntreasure += 1
                else:
                    temphand[z] = cardDrawn
                    # this should just remove the top card (the most recently drawn one).
                    state.handCount[currentPlayer] -= 1
                    z += 1

        while z - 1 >= 0:
            # discard all cards in play that have been drawn
            state.discardCount[currentPlayer] += 1
            state.discard[currentPlayer][state.discardCount[currentPlayer]] = temphand[z-1]
            z -= 1

        return 0

    elif card == enums.Card.councilroom:

        # TODO:

        return 0

    elif card == enums.Card.feast:
        # gain card with cost up to 5
        # Backup hand
        for i in range(state.handCount[currentPlayer] + 1):
            temphand[i] = state.hand[currentPlayer][i]  # Backup card
            state.hand[currentPlayer][i] = -1  # Set to nothing

        # Backup hand
        # Update Coins for Buy
        updateCoins(currentPlayer, state, 5)
        x = 1  # Condition to loop on

        # while x == 1:  # Buy one card
        if supplyCount(choice1, state) <= 0:
            # DEBUG
            print "None of that card left, sorry!\n"

            print "Cards Left: {0:d}\n".format(supplyCount(choice1, state))

        elif state.coins < getCost(choice1):
            print "That card is too expensive!\n"

            # DEBUG
            print "Coins: {0:d} < {1:d}\n".format(state.coins, getCost(choice1))

        else:
            # DEBUG
            print "Deck Count: {0:d}\n".format(state.handCount[currentPlayer] + state.deckCount[currentPlayer] + state.discardCount[currentPlayer])

            result = gainCard(choice1, state, 0, currentPlayer)  # Gain the card
            assert (result != -1), "The returned value of gainCard should not be -1."
            x = 0  # No more buying cards

            # DEBUG
            print "Deck Count: {0:d}\n".format(state.handCount[currentPlayer] + state.deckCount[currentPlayer] + state.discardCount[currentPlayer])

        # Reset Hand
        for i in range(state.handCount[currentPlayer] + 1):
            state.hand[currentPlayer][i] = temphand[i]
            temphand[i] = -1

        return 0

    elif card == enums.Card.gardens:
        return -1

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

                        state.supplyCount[enums.Card.estate] -= 1  # Decrement estates

                        if supplyCount(enums.Card.estate, state) == 0:
                            isGameOver(state)

                    card_not_discarded = 0  # Exit the loop

                else:
                    p += 1  # Next card

        else:
            if supplyCount(enums.Card.estate, state) > 0:
                result = gainCard(enums.Card.estate, state, 0, currentPlayer)  # Gain an estate
                assert (result != -1), "The returned value of gainCard should not be -1."

                state.supplyCount[enums.Card.estate] -= 1  # Decrement Estates

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
        state.supplyCount[state.hand[currentPlayer][choice1]] += choice2

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
        if state.supplyCount[choice1] == -1:
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


def gainCard(supplyPos, state, toFlag, player):

    # Note: supplyPos is enum of chosen card

    # check if supply pile is empty (0) or card is not used in game (-1)
    if supplyCount(supplyPos, state) < 1:
        return -1

    # added card for [whoseTurn] current player:
    # toFlag = 0 : add to discard
    # toFlag = 1 : add to deck
    # toFlag = 2 : add to hand

    if toFlag == 0:
        state.discard[player][state.discardCount[player]] = supplyPos
        state.discardCount[player] += 1

    elif toFlag == 1:
        state.deck[player][state.deckCount[player]] = supplyPos
        state.deckCount[player] += 1

    elif toFlag == 2:
        state.hand[player][state.handCount[player]] = supplyPos
        state.handCount[player] += 1

    else:
        return -1

    # decrease number in supply pile
    state.supplyCount[supplyPos] -= 1

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


# TODO: CHECK THE RETURN VALUE
def updateCoins(player, state, bonus):

    assert isinstance(state, enums.GameState)

    # reset coin count
    state.coins = 0

    for i in range(state.handCout[player]):
        if state.hand[player][i] == enums.Card.copper:
            state.coins += 1
        elif state.hand[player][i] == enums.Card.silver:
            state.coins += 2
        elif state.hand[player][i] == enums.Card.gold:
            state.coins += 3

    # add bonus
    state.coins += bonus

    return 0


# TODO: CHECK THE RETURN VALUE
def drawCard(player, state):

    assert isinstance(state, enums.GameState)

    if state.deckCount[player] <= 0:  # Deck is empty

        # Step 1 Shuffle the discard pile back into a deck

        # Move discard to deck
        for i in range(state.discardCount[player]):
            state.deck[player][i] = state.discard[player][i]
            state.discard[player][i] = -1

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
        count = state.handCount[player]  # Get current hand count for player

        # Debug statements
        print "Current hand count: {0:d}\n".format(count)

        deckCounter = state.deckCount[player]  # Create holder for the deck count
        state.hand[player][count] = state.deck[player][deckCounter - 1]  # Add card to the hand
        state.deckCount[player] -= 1
        state.handCount[player] += 1  # Increment hand count

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