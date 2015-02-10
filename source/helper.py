__author__ = 'liux4@onid.oregonstate.edu'

import enums
import dominion

# NON-API functions
def cardEffect(card, choice1, choice2, choice3, game, handPos, bonus):

    currentPlayer = game.whoseTurn
    nextPlayer = (currentPlayer + 1) % len(game.players)

    tributeRevealedCards = [-1, -1]
    temphand = []  # temphand[MAX_HAND]  # moved above the if statement

    z = 0  # this is the counter for the temp hand

    if card == enums.Card.adventurer:  # 7
        # reveal cards from your deck until you reveal 2 Treasure cards.
        # put those Treasure cards into your hands and discard the other
        # revealed cards.
        drawntreasure = 0
        while drawntreasure < 2:
            if game.players[currentPlayer].deckCount() < 1:
                # if the deck is empty we need to shuffle discard and add to deck
                dominion.shuffle(currentPlayer, game)

            drawCard(currentPlayer, game)

            # top card of hand is most recently drawn card.
            cardDrawn = game.players[currentPlayer].handCards[-1]

            if cardDrawn == enums.Card.copper or cardDrawn == enums.Card.silver or cardDrawn == enums.Card.gold:
                drawntreasure += 1
            else:
                game.players[currentPlayer].handCards.pop(-1)
                game.players[currentPlayer].discardCards.append(cardDrawn)

        game.players[game.whoseTurn].handCards.pop(handPos)
        game.players[game.whoseTurn].discardCards.append(card)

        return 0

    elif card == enums.Card.bureaucrat:  # 8
        # Bureaucrat - If you have no cards left in your Deck when you
        # play this card, the Silver you gain will become the only card in
        # your Deck. Similarly, if another player has no cards in his Deck,
        # the Victory card he puts on top will become the only card in his Deck.

        for i in range(0, len(game.players)):
            if i != currentPlayer:
                for j in range(0, game.players[i].handCardCount()):
                    if enums.Card.estate <= game.players[i].handCards[j] <= enums.Card.province:
                        victory = game.players[i].handCards.pop(j)
                        game.players[i].cardsInDeck.insert(0, victory)
                        handPos += 1
                        break

        game.players[currentPlayer].handCards.pop(handPos)
        game.players[currentPlayer].cardsInDeck.append(card)

        game.players[currentPlayer].silver += 1

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
            if 0 <= choices[i] <= game.players[currentPlayer].handCardCount() - 1 and choices[i] != handPos:
                game.players[currentPlayer].handCards.pop(choices[i])
                if choices[i] < handPos:
                    handPos -= 1

                game.players[currentPlayer].discardCards.append(choices[i])
                newcards += 1

        for i in range(0, newcards):
            drawCard(currentPlayer, game)

        game.players[currentPlayer].handCards.pop(handPos)
        game.players[currentPlayer].discardCards.append(card)
        game.numActions += 1

        return 0

    elif card == enums.Card.chapel:  # 10
        # Chapel - You cannot trash the Chapel itself since it is not in your
        # hand when you resolve it. You could trash a different Chapel card
        # if that card were in your hand.

        for i in range(0, game.players[game.whoseTurn].handCardCount()):
            if handPos != i and enums.Card.chapel == game.players[game.whoseTurn].handCards[i]:
                game.players[game.whoseTurn].trash.append(game.players[game.whoseTurn].handCards.pop(i))
                break

        game.players[currentPlayer].handCards.pop(handPos)
        game.players[currentPlayer].discardCards.append(card)

        return 0

    elif card == enums.Card.chancellor:  # 11
        # Chancellor - You must resolve the Chancellor (decide whether or
        # not to discard your Deck by flipping it into your Discard pile)
        # before doing other things on your turn, like deciding what to
        # buy or playing another Action card. You may not look through
        # your Deck as you discard it.

        game.players[currentPlayer].handCards.pop(handPos)
        game.players[currentPlayer].discardCards.append(card)

        game.players[currentPlayer].coins += 2

        game.players[currentPlayer].discardCards.extend(game.players[currentPlayer].cardsInDeck)
        game.players[currentPlayer].cardsInDeck = []

        return 0

    elif card == enums.Card.councilroom:  # 12
        # Council Room -The other players must draw a card whether
        # they want to or not. All players should shuffle as necessary.

        for i in range(0, len(game.players)):
            if i != currentPlayer:
                drawCard(i, game)

        game.players[currentPlayer].handCards.pop(handPos)
        game.players[currentPlayer].discardCards.append(card)

        return 0

    elif card == enums.Card.feast:  # 13
        # The gained card goes into your Discard pile. It has to be a
        # card from the Supply. You cannot use coins from Treasures or
        # previous Actions (like the Market) to increase the cost of the
        # card that you gain.

        # temphand = copy.deepcopy(game.players[currentPlayer].handCards)
        #
        # game.players[currentPlayer].handCards = []

        coins = game.players[currentPlayer].coins

        # Backup hand
        # Update Coins for Buy
        updateCoins(currentPlayer, game, 5)

        # Buy one card
        count = dominion.supplyCount(choice1, game)
        if count <= 0:
            game.error = "None of that card left!"
            return -1

        elif game.players[currentPlayer].coins < getCost(choice1):
            game.error = "That card is too expensive!"
            return -1

        else:
            gainCard(choice1, game, 0, currentPlayer)  # Gain the card and put it into discard cards

        if coins < game.players[currentPlayer].coins:
            game.players[currentPlayer].coins = coins

        game.players[currentPlayer].handCards.pop(handPos)
        game.players[currentPlayer].discardCards.append(card)

        return 0

    elif card == enums.Card.festival:  # 14
        # Festival - it gives both 2 actions, 2 coins, and 1 Buy.

        game.numActions += 2
        game.numBuys += 1
        game.players[currentPlayer].coins += 2

        game.players[currentPlayer].handCards.pop(handPos)
        game.players[currentPlayer].discardCards.append(card)

        return 0

    elif card == enums.Card.gardens:  # 15
        return -1

    elif card == enums.Card.laboratory:  # 16
        # Laboratory - It increases your handsize by giving you +2 cards,
        # and then gives +1 action so you can keep playing more actions.
        game.players[currentPlayer].handCards.pop(handPos)
        game.players[currentPlayer].discardCards.append(card)

        game.numActions += 2

        drawCard(currentPlayer, game)
        drawCard(currentPlayer, game)

        return 0

    elif card == enums.Card.seahag:  # 17
        # Seahag - Each other player discards the top card of his deck,
        # then gains a Curse card, putting it on top of his deck.

        for i in range(0, len(game.players)):
            if i != currentPlayer:
                discard = game.players[i].cardsInDeck.pop(-1)
                game.players[i].discardCards.append(discard)

                game.players[i].cardsInDeck.append(enums.Card.curse)
                game.supplies.curseCount -= 1

        game.players[currentPlayer].handCards.pop(handPos)
        game.players[currentPlayer].discardCards.append(card)

        return 0

    elif card == enums.Card.smithy:  # 18
        # Smithy - it increases your handsize by drawing 3 cards

        game.players[currentPlayer].handCards.pop(handPos)
        game.players[currentPlayer].discardCards.append(card)

        # +3 Cards
        for i in range(3):
            drawCard(currentPlayer, game)

        return 0

    elif card == enums.Card.village:  # 19
        # Village - it generate +2 actions and +1 Card.

        game.players[currentPlayer].handCards.pop(handPos)
        game.players[currentPlayer].discardCards.append(card)

        # +1 Card
        drawCard(currentPlayer, game)

        # +2 Actions
        game.numActions += 2

        return 0


def gainCard(card, game, toFlag, player):

    # Note: card is enum of chosen card

    # check if supply pile is empty (0) or card is not used in game (-1)
    if dominion.supplyCount(card, game) < 1:
        return -1

    # added card for [whoseTurn] current player:
    # toFlag = 0 : add to discard
    # toFlag = 1 : add to deck
    # toFlag = 2 : add to hand

    if toFlag == 0:
        game.players[player].discardCards.append(card)
        # game.discard[player][game.discardCount[player]] = card
        # game.discardCount[player] += 1

    elif toFlag == 1:
        game.players[player].cardsInDeck.append(card)

        # game.deck[player][game.deckCount[player]] = card
        # game.deckCount[player] += 1

    elif toFlag == 2:
        game.players[player].handCards.append(card)

        # game.hand[player][game.handCount[player]] = card
        # game.handCount[player] += 1

    else:
        return -1

    # decrease number in supply pile
    if game.supplies.updateSupplyCount(card, 1) == -1:
        game.error = "Failed to update the count of card: {0:d}.".format(card)
        return -1

    return 0


def updateCoins(player, game, bonus):

    for i in range(0, game.players[player].handCardCount()):
        if game.players[player].handCards[i] == enums.Card.copper:
            game.players[player].coins += 1
        elif game.players[player].handCards[i] == enums.Card.silver:
            game.players[player].coins += 2
        elif game.players[player].handCards[i] == enums.Card.gold:
            game.players[player].coins += 3

    # add bonus
    game.players[player].coins += bonus

    return 0


def drawCard(player, game):

    if game.players[player].deckCount() <= 0:  # Deck is empty

        # Step 1 Shuffle the discard pile back into a deck

        # Move discard to deck
        game.players[player].cardsInDeck.append(game.players[player].discardCards)
        game.players[player].discardCards = []

        game.deckCount[player] = game.discardCount[player]
        game.discardCount[player] = 0  # Reset discard

        # Shuffle the deck
        dominion.shuffle(player, game)  # Shuffle the deck up and make it so that we can draw

        # Debug statements
        print "Deck count now: {0:d}\n".format(game.deckCount[player])

        game.discardCount[player] = 0

        # Step 2 Draw Card
        count = game.handCount[player]  # Get current player's hand count

        # Debug statements
        print "Current hand count: {0:d}\n".format(count)

        deckCounter = game.deckCount[player]  # Create a holder for the deck count

        if deckCounter == 0:
            return -1

        game.hand[player][count] = game.deck[player][deckCounter - 1]  # Add card to hand
        game.deckCount[player] -= 1
        game.handCount[player] += 1  # Increment hand count

    else:
        card = game.players[player].cardsInDeck.pop(0)
        game.players[player].handCards.append(card)

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
    elif card == enums.Card.bureaucrat:
        return 4
    elif card == enums.Card.cellar:
        return 2
    elif card == enums.Card.chapel:
        return 2
    elif card == enums.Card.chancellor:
        return 3
    elif card == enums.Card.councilroom:
        return 5
    elif card == enums.Card.feast:
        return 4
    elif card == enums.Card.festival:
        return 5
    elif card == enums.Card.gardens:
        return 4
    elif card == enums.Card.laboratory:
        return 5
    elif card == enums.Card.seahag:
        return 4
    elif card == enums.Card.smithy:
        return 4
    elif card == enums.Card.village:
        return 3
    else:
        return -1
