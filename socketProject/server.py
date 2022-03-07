import socket
import threading
import random

from numpy import number

PORT = 31250
SERVER = "169.254.120.74" # pi ip
#SERVER = "169.254.131.107" #windows ip
HEADER = 64 #tells length of message
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def send(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' *  (HEADER - len(send_length))
    conn.send(send_length) #this is the header that tells how long the next message will be
    conn.send(message)

    
# Game logic stuff here
class player: #player has their name and their hand of cards
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

    def __init__(self):
        self.deck = board_state.deckstrs.copy() #take a fresh deck for this instance of the board
        self.discard = []
        self.players = {player("testplayer")}
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
def send_board(board): 
    pass
def play_game(players, board): #play game takes a player object for this thread and then a board state shared between players
    for player in players:
        board.register_player(player)
    for player in players: #give each player two cards
        player.hand.append(board.deck.pop())
        player.hand.append(board.deck.pop())
        send(player.conn("the board state is: "))

    
def handle_message(conn, message):
    message = message.split()
    global reg_players #global so it can be used in all threads
    global main_board #global so it can be used in all threads
    reg_players = []
    if message[0] == "register":
        print('register handler')
        reg_players.append(player(message[1], conn))
    elif message[0] == "query" and message[1] == "players":
        print('query players handler')
    elif message[0] == "start" and message[1] == "game":
        print('start game handler')
        main_board = board_state()
        play_game(reg_players, main_board)
    elif message[0] == "query" and message[1] == "games":
        print('query games handler')
    elif message[0] == "end":
        print('end game handler')
    elif message[0] == "de-register":
        print('de-register handler')

#networking receiver here
def handle_client(conn, addr):
    print(f"new connection: {addr} connected")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
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