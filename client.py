import socket
import threading
import logging
import logging.config


SERVER_PORT = 12343

logging.config.fileConfig("logger.conf")
logger = logging.getLogger("logger")


def main():
    uname = input("Username: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("Server IP: ")
    sock.connect((server_ip, SERVER_PORT))
    logger.info(f"Trying to connect to {server_ip}:{SERVER_PORT}")
    sock.send(uname.encode())
    print(sock.recv(1024).decode())


if __name__ == "__main__":
    main()
