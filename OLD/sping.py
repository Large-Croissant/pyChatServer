import socket
import time

SERVER_IP = "localhost"
SERVER_PORT = 12321

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(1)
    while True:
        client, addr = server.accept()
        print(f"Client {addr[0]}:{addr[1]} connected")
        time.sleep(2)
        client.send(b"ping")
        recv = client.recv(128)
        if recv == b"pong":
            print("Ping success")
        else:
            print("Ping fail")
        client.close()

if __name__ == "__main__":
    main()