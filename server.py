import socket
import threading
import logging
import logging.config


SERVER_PORT = 12343
BIND_ADDR = "0.0.0.0"

logging.config.fileConfig("logger.conf")
logger = logging.getLogger("logger")

CLIENTS = []


class User:
    def __init__(self, uname: str, sock: socket.socket, addr: tuple):
        """
        Initialize a User instance.

        :param uname: The username of the client
        :param sock: The socket object associated with the client
        :param addr: The address (IP, port) of the client
        """
        self.uname = uname
        self.sock = sock
        self.addr = addr

    def __str__(self):
        """
        String representation of the User instance.
        """
        return f"User(username={self.uname}, addr={self.addr})"


def auth_client(sock: socket.socket, addr: tuple):
    uname = sock.recv(512).decode()
    if any(user.uname == uname for user in CLIENTS):
        logger.info(f"Denied connection from {addr[0]}:{addr[1]} becuase {uname} is already taken")
    else:
        user = User(uname, sock, addr)
        CLIENTS.append(user)
        logger.info(f"User {uname} connected from {addr[0]}:{addr[1]}")
        sock.send(f"[SERVER] Hello, {uname} :)".encode())


def listen_for_clients(sock: socket.socket):
    sock.listen()
    logger.info("Listener started")
    while True:
        client_sock, client_addr = sock.accept()
        logger.info(f"Client trying to connect from {client_addr[0]}:{client_addr[1]}")
        auth_thread = threading.Thread(target=auth_client, args=[client_sock, client_addr])
        auth_thread.start()


def main():
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind((BIND_ADDR, SERVER_PORT))
    logger.info(f"Listener socket created and bound to {BIND_ADDR}")
    listen_thread = threading.Thread(target=listen_for_clients, args=[listen_sock])
    listen_thread.start()


if __name__ == "__main__":
    main()
