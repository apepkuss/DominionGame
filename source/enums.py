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
    adventurer = 7    # action card
    bureaucrat = 8    # action attack card
    cellar = 9        # action card
    chapel = 10       # action card
    chancellor = 11   # action card
    councilroom = 12  # action card
    feast = 13        # action card
    festival = 14     # action card
    gardens = 15  # not action card
    laboratory = 16   # action card
    seahag = 17       # action attack card
    smithy = 18       # action card
    village = 19      # action card


class GamePhase(Enum):
    action = 0
    buy = 1
    cleanup = 2
    unknown = 3


class GameState:

    def __init__(self, playerCount):
        self.players = {}
        self.supplies = Supply()
        self.whoseTurn = 0  # 0: player1; 1: player2
        self.phase = GamePhase.unknown
        self.numActions = 1  # Starts at 1 each turn
        self.numBuys = 1  # Starts at 1 each turn
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
        self.trash = []

        self.gold = 0
        self.silver = 0
        self.copper = 0
        self.coins = 0

        self.estateCount = 0
        self.duchyCount = 0
        self.provinceCount = 0

        self.credits = 0

    def handCardCount(self):
        return len(self.handCards)

    def discardCardCount(self):
        return len(self.discardCards)

    def deckCount(self):
        return len(self.cardsInDeck)
