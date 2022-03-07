import random
class board_state:
    number_of_games = 0
    registered_users = []
    #setup dictionary is used to create the deck and get card values
    decknums = list(range(1,53))
    deckvals = list(range(1,14))*4
    for i in range(len(deckvals)): #sets value 2 to be -2 value
        if deckvals[i] == 2:
            deckvals[i] = -2
    deckstrs = []
    for cardnum in decknums:
        if (cardnum >= 1 and cardnum <= 13):
            suit = 'D'
            suitmod = 0
        elif (cardnum >= 14 and cardnum <= 26):
            suit = 'C'
            suitmod = 13
        elif (cardnum >= 27 and cardnum <= 39):
            suit = 'H'
            suitmod = 26
        elif (cardnum >= 40 and cardnum <= 52):
            suit = 'S'
            suitmod = 39
        if(deckvals[cardnum-1] <= 9):
            deckstrs.append(" " + str(cardnum-suitmod) + suit)
        else:
            deckstrs.append(str(cardnum-suitmod) + suit)
    dict_deck = dict(zip(deckstrs, deckvals)) #this creates a dictionary of cards and their values, access the value with deck[" 3D"]

    def __init__(self, dealer, k):
        self.deck = board_state.deckstrs
        self.discard = []
        self.numPlayers = k
        self.dealer = dealer
        self.players = []
    def shuffle_deck(self):
        random.shuffle(self.deck)
    def draw_card(self):
        return self.deck.pop()
    def discard_card(self, card):
        self.discard.append(card)
    def add_player(self,player):
        self.players.append(player)