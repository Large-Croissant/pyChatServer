import socket

SERVER_IP = "localhost"
SERVER_PORT = 12321

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    while True:
        recv = sock.recv(128)
        if recv == b"ping":
            print("ping received")
            sock.send(b"pong")
            sock.close()
            break
        

if __name__ == "__main__":
    main()