import socket
import threading
import random

from numpy import number

PORT = 31250
SERVER = "169.254.120.74" # pi ip
#SERVER = "169.254.131.107" #windows ip
FORMAT = 'utf-8'
MSG_LENGTH = 2048
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

global reg_players #global so it can be used in all threads
global main_board #global so it can be used in all threads
reg_players = []
def send(conn, msg):
    message = msg.encode(FORMAT)
    conn.send(message)

# Game logic stuff here
class player_class: #player has their name and their hand of cards
    def __init__(self, name, conn):
        self.hand = []
        self.name = name
        self.total_points = 0
        self.game_points = 0
        self.conn = conn
    def send_hand(self):
        send(self.conn, self.hand)
class board_state:
    number_of_games = 0
    registered_players = []
    #setup dictionary is used to create the deck and get card values
    decknums = list(range(1,53))
    deckvals = list(range(1,14))*4
    for i in range(len(deckvals)): #sets value 2 to be -2 value
        if deckvals[i] == 2:
            deckvals[i] = -2
    deckstrs = []
    for cardnum in decknums: #letter represents suit, space is for padding between cards
        if (cardnum >= 1 and cardnum <= 13):
            suit = 'D '
            suitmod = 0
        elif (cardnum >= 14 and cardnum <= 26):
            suit = 'C '
            suitmod = 13
        elif (cardnum >= 27 and cardnum <= 39):
            suit = 'H '
            suitmod = 26
        elif (cardnum >= 40 and cardnum <= 52):
            suit = 'S '
            suitmod = 39
        if(deckvals[cardnum-1] <= 9):
            deckstrs.append(" " + str(cardnum-suitmod) + suit)
        else:
            deckstrs.append(str(cardnum-suitmod) + suit)
    dict_deck = dict(zip(deckstrs, deckvals)) #this creates a dictionary of cards and their values, access the value with deck[" 3D"]

    def __init__(self):
        self.deck = board_state.deckstrs.copy() #take a fresh deck for this instance of the board
        self.discard = []
        self.players = []
    def shuffle_deck(self):
        random.shuffle(self.deck)
    def discard_card(self, card):
        self.discard.append(card)
    def register_player(self, name): #add a player to registered players list
        self.registered_players.append(name)
    #def add_player(self,name): #add a player to a game and give it a connection
        #self.players.append(player(name))
    def play(self):
        for player in self.players: #give each player two cards
            player.hand.append(self.deck.pop())
            player.hand.append(self.deck.pop())
        #loop until each player has 6 cards. in each iteration ask the player whether they want to flip a card or take from the discard.
def send_board(player, board): 
    send_string = f"player {player.name}'s hand:\n"
    for card in player.hand:
        send_string = send_string + card
    num_cards = len(player.hand)
    for c in range(6 - num_cards):
        if c + num_cards == 3:
            send_string = send_string + "\n"
        send_string = send_string + "*** "
    send_string = send_string + "\n"
    send(player.conn, send_string)
        
def play_game(players, board): #play game takes a player object for this thread and then a board state shared between players
    for player in players:
        board.register_player(player)
    for player in players: #give each player two cards
        player.hand.append(board.deck.pop())
        player.hand.append(board.deck.pop())
        send_board(player,board)

 
def handle_message(conn, message):
    message = message.split()

    if message[0] == "register":
        print('register handler')
        tempplayer = player_class(message[1], conn)
        reg_players.append(tempplayer)
        print('registered players:')
        send(conn, f"\n[RESPONSE] player {message[1]} registered on ip {message[2]} on port {message[3]}")
        #for player in reg_players:
            #print(player.name)
    elif message[0] == "query" and message[1] == "players":
        print('query players handler')
    elif message[0] == "start" and message[1] == "game":
        print('start game handler')
        main_board = board_state()
        main_board.shuffle_deck()
        play_game(reg_players, main_board)
    elif message[0] == "query" and message[1] == "games":
        print('query games handler')
    elif message[0] == "end":
        print('end game handler')
    elif message[0] == "de-register":
        print('de-register handler')
    else:
        send(conn, "command not understood")
    return True
#networking receiver here
def handle_client(conn, addr):
    print(f"new connection: {addr} connected")
    connected = True
    while connected:
        msg = conn.recv(MSG_LENGTH).decode(FORMAT)
        connected = handle_message(conn, msg)
    conn.close()
#begin the program
def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        print(f"connection: {conn} at address: {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"active connections {threading.activeCount() - 1}")
print("server is starting")
start()