import socket

SERVER_IP = "localhost"
SERVER_PORT = 42069

def main():
    uname = input("Enter your username: ")
    try:
        print("Attempting to connect to server...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, SERVER_PORT))
    except:
        print(f"Failed to connect to {SERVER_IP} on port {SERVER_PORT}")
        exit(1)
    print(f"Connected to server ({SERVER_IP}:{SERVER_PORT})")
    sock.send(uname.encode())
    
    while True:
        recv = sock.recv(2048)
        if recv == b"DISCONNECT":
            sock.close()
            break
        elif recv == b"ping":
            sock.send(b"pong")
        else:
            print(recv.decode())
    print("Disconnected from server")

if __name__ == "__main__":
    main()