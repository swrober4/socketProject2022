import socket
import threading
from time import sleep
#networking stuff 
PORT = 31250
SERVER = "169.254.120.74" # pi ip
#SERVER = "169.254.131.107" #windows ip
FORMAT = 'utf-8'
MSG_LENGTH = 2048
ADDR = (SERVER, PORT)
#game logic stuff

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)
def handle_server(): #This is called in its own thread and waits for server responses, then parses them to a handler
    connected = True
    while connected:
        msg = client.recv(MSG_LENGTH).decode(FORMAT)
        if msg == 'disconnect':
            connected = False
        else:
            print(msg)

def start():
    thread = threading.Thread(target=handle_server) #client has 2 threads, one for sending messages to server and one for handling responses
    thread.start()
    while(True):
        message_to_server = input()
        send(message_to_server)

start()