import socket
import threading

SERVER_IP = "localhost"
SERVER_PORT = 42069

CLIENTS = dict() # username : (client_socket, client_thread, ip, port)

def process_connections(server_sock: socket.socket, stop_server_event: threading.Event):
    while not stop_server_event.is_set():
        client, addr = server_sock.accept()
        client_ip = addr[0]
        client_port = addr[1]
        print(f"Connected to {client_ip} on port {client_port}")
        client_thread = None
        client_thread = threading.Thread(target=process_client, args=(client, client_ip, client_port, client_thread))
        client_thread.start()

def ping(sock: socket.socket) -> bool:
    sock.send(b"ping")
    recv = sock.recv(64)
    if recv == b"pong":
        return True
    return False

def process_client(client_sock: socket.socket, ip: str, port: int, client_thread: threading.Thread):
    # uname = ""
    # while True:
    #     uname = client_sock.recv(256).decode()
    #     if uname in CLIENTS:
    #         client_sock.send("Username already taken")
    #         client_sock.send(b"DISCONNECT")
    #         client_sock.close()
    #         client_thread.join()
    #     else:
    #         break
    uname = client_sock.recv(128).decode()
    print(f"{ip}:{port} is [{uname}]")
    client_sock.send(f"Hello, {uname}".encode())
    CLIENTS[uname] = (client_sock, client_thread, ip, port)
    print(CLIENTS[uname])
    while ping(client_sock):
        print(client_sock.recv(2048).decode())
    print(f"Client {uname} ({ip}:{port}) disconnected")
    client_sock.close()
    client_thread.join()  

def server_controls(stop_event: threading.Event):
    while True:
        try:
            cmd = input()
            if cmd == "close_server":
                stop_event.set()
                for client in CLIENTS:
                    client_socket, client_thread, ip, port = CLIENTS[client]
                    client_socket.send(b"DISCONNECT")
                    client_socket.close()
                    client_thread.join()
                    print(f"Closed connection with [{client}] ({ip}:{port})")
                break
            elif cmd.split()[0] == "disconnect_client":
                to_disconnect = " ".join(cmd.split()[1:])
                print(to_disconnect)
                client_socket, client_thread, ip, port = CLIENTS[to_disconnect]
                client_sock.send(b"DISCONNECT")
                client_sock.close()
                client_thread.join()
                print(f"Disconnected [{to_disconnect}] ({ip}:{port})")
            elif cmd == "list_clients":
                for client in CLIENTS:
                    _, _, ip, port = CLIENTS[client]
                    print(f"\t[{client}] ({ip}:{port})")
            elif cmd.split()[0] == "send":
                client_name = " ".join(cmd.split()[1:])
                message: str = input("Message: ")
                client_sock: socket.socket = CLIENTS[client_name][0]
                print(f"Sent \"{message}\" to {client}")
                client_sock.send(*message.encode())
            else:
                print(f"Unknown command \"{cmd}\"")
        except:
            pass

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((SERVER_IP, SERVER_PORT))
    server_sock.listen(20)
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")
    print("Waiting for connections...")
    stop_server_event = threading.Event()
    process_connections_thread = threading.Thread(target=process_connections, args=(server_sock, stop_server_event))
    process_connections_thread.start()
    server_controls(stop_server_event)
    process_connections_thread.join()

if __name__ == "__main__":
    main()