__author__ = 'liux4@onid.oregonstate.edu'

from enum import Enum


class Card(Enum):
    curse = 0
    estate = 1
    duchy = 2
    province = 3

    copper = 4
    silver = 5
    gold = 6

    adventurer = 7
    # If no/only 1 treasure found, stop when full deck seen.
    councilroom = 8
    feast = 9  # choice1 is supply # of card gained.
    gardens = 10
    mine = 11  # choice1 is hand* of money to trash, choice2 is supply* of money to put in hand
    remodel = 12  # choice1 is hand* of card to remodel, choice2 is supply*
    smithy = 13
    village = 14

    baron = 15  # choice1: boolean for discard of estate
    #  Discard is always of first (lowest index) estate
    greathall = 16
    minion = 17  # choice1:  1 = +2 coin, 2 = redraw
    steward = 18  # choice1: 1 = +2 card, 2 = +2 coin, 3 = trash 2 (choice2,3)
    tribute = 19

    ambassador = 20  # choice1 = hand#, choice2 = number to return to supply.
    cutpurse = 21
    embargo = 22  # choice1 = supply*
    outpost = 23
    salvanger = 24  # choice1 = hand# to trash
    seahag = 25
    treasuremap = 26


class GameState:

    def __init__(self):
        pass

    players = 0  # number of players
    supplyCount = []  # this is the amount of a specific type of card given a specific number.
    embargoTokens = []
    outpostPlayed = 0
    outpostTurn = 0
    whoseTurn = 0
    phase = 0
    numActions = 1  # Starts at 1 each turn
    coins = 0  # Use as you see fit!
    numBuys = 1  # Starts at 1 each turn
    hand = [[]]
    handCount = []
    deck = [[]]
    deckCount = [[]]
    discard = [[]]
    discardCount = []
    playedCards = []
    playedCardCount = 0

