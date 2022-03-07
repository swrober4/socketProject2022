import socket
import threading
from time import sleep
#networking stuff 
PORT = 31250
SERVER = "169.254.120.74" # pi ip
#SERVER = "169.254.131.107" #windows ip
HEADER = 64 #tells length of message
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
#game logic stuff

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' *  (HEADER - len(send_length))
    client.send(send_length) #this is the header that tells how long the next message will be
    client.send(message)

def handle_server(): #This is called in its own thread and waits for server responses, then parses them to a handler
    connected = True
    while connected:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            print(f"Server sent message {msg}")
            if msg == 'disconnect':
                connected = False

def start():
    thread = threading.Thread(target=handle_server) #client has 2 threads, one for sending messages to server and one for handling responses
    thread.start()
    while(True):
        message_to_server = input("input (for help type 'help'): ")
        send(message_to_server)

start()