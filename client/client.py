import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# init colorama colors
init();

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
];

# choose a random client color
client_color = random.choice(colors);


# server IP address
SERVER_HOST = "127.0.0.1";
SERVER_PORT = 22231;
separator_token = "<:::>";

# initialize TCP socket
s = socket.socket();
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...");
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT));
print("[+] Connected.")

# prompt the client for a name
name = input("Enter your name: ")


def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()


while True:
    # input message we want to send to the server
    to_send =  input()
    # a way to exit the program
    if to_send.lower() == 'q' or to_send.lower() == 'exit' or to_send.lower() == 'quit':
        break

    # a way to change colors
    if to_send.lower() == '/random_color':
        client_color = random.choice(colors);
        to_send = '';


    if to_send != '':
        # add the datetime, name & the color of the sender
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
        # finally, send the message
        s.send(to_send.encode())

# close the socket
s.close()