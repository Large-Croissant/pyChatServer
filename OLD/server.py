import socket
import threading

SERVER_IP = "localhost"
SERVER_PORT = 42069

CLIENTS = dict() # username : (client_socket, client_thread, ip, port)

def handshake_with_client(sock: socket.socket, addr: tuple) -> tuple:
    ip = addr[0]
    port = addr[1]
    # get username
    uname = sock.recv(256)
    if uname in CLIENTS:
        sock.send(f"Username \"{uname}\" already taken, disconnecting...".encode())
        sock.send(b"DISCONNECT")
        print(f"{ip}:{port} tried to connect with taken username [{uname}]")
        return None, None, None
    else:
        sock.send(f"Hello, [{uname}]")
        return uname, ip, port

def process_connections(stop_server_event: threading.Event, server_sock: socket.socket):
    # listen for connections
    while not stop_server_event.is_set():
        client_sock, client_addr = server_sock.accept()
        uname, ip, port = handshake_with_client(client_sock, client_addr)
        # connect if handshake was good
        if uname is not None:
            client_thread = threading.Thread(target=process_client, args=(client_sock, uname))
            CLIENTS[uname] = (client_sock, client_thread, ip, port)
            client_thread.start()

    # disconnect with all clients when server stops
    for client in CLIENTS:
        client_socket, client_thread, client_ip, client_port = CLIENTS[client]
        client_socket.close()
        client_thread.join()
        print(f"Closed connection with [{client}] ({client_ip}:{client_port})")

def client_listen():
    pass

def client_send():
    pass

def process_client(sock: socket.socket, uname: str):
    sock.send(f"Hello, {uname}")
    sock.close()
    # do listen and send

def server_controls():
    pass

def main():
    # server sock setup
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((SERVER_IP, SERVER_PORT))
    server_sock.listen(20)
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")

    print("Waiting for connections...")
    stop_server_event = threading.Event()
    process_connections_thread = None
    process_connections_thread = threading.Thread(target=process_connections, args=(stop_server_event, server_sock))
    process_connections_thread.start()
    server_controls(stop_server_event)
    process_connections_thread.join()

if __name__ == "__main__":
    main()