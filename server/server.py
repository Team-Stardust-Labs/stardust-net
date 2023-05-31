import socket;
from threading import Thread;

# server data
SERVER_HOST = "0.0.0.0";    # server ip
SERVER_PORT = 22231;        # server port
separator_token = "<:::>"   # separation of client name and text

# initialize a set of all client sockets
client_sockets = set();
# create a TCP socket
s = socket.socket();
# set the port to be reusable
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT));
# listen for connections
s.listen(5);
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}");


def listen_for_client(cs : socket.socket):
    """
    This function listens for a message from 'cs' socket
    When a message is received, broadcast it to all clients
    """

    while True:
        try:
            # keep listening for a message from 'cs' socket
            msg = cs.recv(1024).decode();
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] {e}");
            client_sockets.remove(cs);
        else:
            # if we received a message, replace the separator
            # token with ": " for better printing
            msg = msg.replace(separator_token, ": ");
        # iterate over all connected sockets
        for client_socket in client_sockets:
            # send the message
            client_socket.send(msg.encode());



while True:
    # listen for new connections
    client_socket, client_address = s.accept();
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket);
    # start a thread that listens for each client's message
    t = Thread(target=listen_for_client, args=(client_socket,));
    # make the thread a daemon so it ends when main thread ends
    t.daemon = True;
    # start the thread
    t.start();


# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()