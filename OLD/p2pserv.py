import socket
import threading

SERVER_IP = "localhost"
SERVER_PORT = 12345

def main():
    uname = input("Username: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen(1)
    while True:
        client, addr = sock.accept()
        client_ip = addr[0]
        client_port = addr[1]
        client.send(uname.encode())
        client_uname = client.recv(256).decode()
        print(f"Connected to [{client_uname}] ({client_ip}:{client_port})\n")
        while True:
            recv = client.recv(2048)
            if recv == b"DISCONNECT":
                client.close()
                break
            else:
                print(recv.decode())

if __name__ == "__main__":
    main()