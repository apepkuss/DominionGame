__author__ = 'liux4@onid.oregonstate.edu'

from enum import Enum

MAX_PLAYERS = 4


class Card(Enum):

    curse = 0

    estate = 1
    duchy = 2
    province = 3

    copper = 4
    silver = 5
    gold = 6

    # kingdom cards
    adventurer = 7
    bureaucrat = 8  # action attack card
    cellar = 9
    chapel = 10
    chancellor = 11
    councilroom = 12
    feast = 13
    festival = 14
    gardens = 15  # not action card
    laboratory = 16
    library = 17
    market = 18
    militia = 19
    mine = 20
    moat = 21
    moneylender = 22
    remodel = 23
    smithy = 24
    spy = 25
    thief = 26
    throneroom = 27
    village = 28
    witch = 29
    woodcutter = 30
    workshop = 31

    # baron = 31  # choice1: boolean for discard of estate
    # #  Discard is always of first (lowest index) estate
    # greathall = 32
    # minion = 33  # choice1:  1 = +2 coin, 2 = redraw
    # steward = 34  # choice1: 1 = +2 card, 2 = +2 coin, 3 = trash 2 (choice2,3)
    # tribute = 35
    #
    # ambassador = 36  # choice1 = hand#, choice2 = number to return to supply.
    # cutpurse = 37
    # embargo = 38  # choice1 = supply*
    # outpost = 39
    # salvanger = 40  # choice1 = hand# to trash
    # seahag = 41

    treasuremap = 41


class GamePhase(Enum):
    action = 0
    buy = 1
    cleanup = 2
    unknown = 3


class GameState:

    def __init__(self, playerCount):
        self.players = {}
        self.supplies = Supply()
        self.embargoTokens = []
        self.outpostPlayed = 0
        self.outpostTurn = 0
        self.whoseTurn = 0  # 0: player1; 1: player2
        self.phase = GamePhase.unknown
        self.numActions = 1  # Starts at 1 each turn
        self.coins = 0  # the money you have
        self.numBuys = 1  # Starts at 1 each turn
        self.hand = [[]]
        self.handCount = []  # the number of cards current player has in hand
        # self.deck = [[]]
        # self.deckCount = [[]]
        # self.discard = [[]]
        # self.discardCount = []
        self.playedCards = []
        self.playedCardCount = 0
        self.error = ""

        self.createPlayers(playerCount)

    def createPlayers(self, playerCount):
        if playerCount > MAX_PLAYERS or playerCount < 2:
            self.error = "The number of players should be 2, 3, or 4."
        else:
            if playerCount > 0:
                for i in range(playerCount):
                    self.players[i] = GamePlayer()


class Supply:

    def __init__(self):

        # 252 kingdom cards =
        # 240 action cards (10 of each) + 12 victory cards (namely, 12 garden cards)
        self.kingdoms = []
        self.adventurerCount = -1
        self.bureaucratCount = -1  # action attack card
        self.cellarCount = -1
        self.chapelCount = -1
        self.chancellorCount = -1
        self.councilroomCount = -1
        self.feastCount = -1
        self.festivalCount = -1
        self.gardensCount = -1  # victory cards
        self.laboratoryCount = -1
        self.libraryCount = -1
        self.marketCount = -1
        self.militiaCount = -1
        self.mineCount = -1
        self.moatCount = -1  # action-reaction card
        self.moneylenderCount = -1
        self.remodelCount = -1
        self.smithyCount = -1
        self.spyCount = -1
        self.thiefCount = -1
        self.throneroomCount = -1
        self.villageCount = -1
        self.witchCount = -1
        self.woodcutterCount = -1
        self.workshopCount = -1

        # 10 Curse cards in the Supply for a 2 player game,
        # 20 Curse cards for 3 players, and
        # 30 Curse cards for 4 players.
        self.curseCount = 0

        # 48 Victory cards
        # After each player takes 3 Estate cards,
        # 3 or 4 player game: 12 Estate, 12 Duchy, and 12 Province cards in the Supply.
        # 2 player game: 8 Estate, 8 Duchy, and 8 Province cards in the Supply.
        self.estateCount = 0
        self.duchyCount = 0
        self.provinceCount = 0

        # 130 Treasure cards
        # After each player takes 7 Copper cards,
        # place the remaining Copper cards and
        # all of the Silver cards and Gold cards
        # in face-up piles in the Supply.
        self.copperCount = 60
        self.silverCount = 40
        self.goldCount = 30

        # self.baronCount = 0
        # self.greathallCount = 0
        # self.minionCount = 0
        # self.stewardCount = 0
        # self.tributeCount = 0
        # self.ambassadorCount = 0
        # self.cutpurseCount = 0
        # self.embargoCount = 0
        # self.outpostCount = 0
        # self.salvangerCount = 0
        # self.seahagCount = 0
        # self.treasuremapCount = 0

    def setSupplyKingdoms(self, kingdomcards):
        for i in range(0, len(kingdomcards)):
            self.kingdoms.append((int(kingdomcards[i]), 10))


    def updateSupplyCount(self, card, count):

        # curse card
        if card == Card.curse:
            self.curseCount -= count

        # Victory cards
        elif card == Card.estate:
            self.estateCount -= count
        elif card == Card.duchy:
            self.duchyCount
        elif card == Card.province:
            self.provinceCount

        # Treasure cards
        elif card == Card.copper:
            self.copperCount
        elif card == Card.silver:
            self.silverCount
        elif card == Card.gold:
            self.goldCount

        # Kingdom cards
        elif Card.adventurer <= card <= Card.workshop:
            self.kingdoms[card]
        else:
            return -1

        return 0

class GamePlayer:

    def __init__(self):
        self.handCards = []
        self.discardCards = []
        self.cardsInDeck = []  # (cardName, cardCount)

        self.gold = 0
        self.silver = 0
        self.copper = 0
        self.coins = 0

        self.estateCount = 0
        self.duchyCount = 0
        self.provinceCount = 0

        self.trash = []

    def handCardCount(self):
        return len(self.handCards)

    def discardCardCount(self):
        return len(self.discardCards)

    def deckCount(self):
        return len(self.cardsInDeck)
