import socket
import threading

SERVER_IP = "localhost"
SERVER_PORT = 42069

def process_connections(server_sock: socket.socket, threads: list[threading.Thread], stop_server: threading.Event, clients: dict):
    while not stop_server.is_set():
        client, addr = server_sock.accept()
        client_ip = addr[0]
        client_port = addr[1]
        print(f"Connected to {client_ip} on port {client_port}")
        thread = threading.Thread(target=process_client, args=(client, client_ip, client_port, clients))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.close()

def process_client(client: socket.socket, ip: str, port: int, clients: dict):
    uname = client.recv(256).decode()
    print(f"{ip}:{port} is [{uname}]")
    client.send(f"Hello, {uname}".encode())
    clients[uname] = (client, (ip, port))
    while True:
        print(client.recv(2048).decode())
    # client.close()
    # print(f"Closed {ip}:{port} ({uname})")

def server_controls(stop_event: threading.Event, clients: dict[str : (socket.socket, tuple[str, int])]):
    while True:
        try:
            cmd = input()
            if cmd == "CLOSE_SERVER":
                stop_event.set()
                break
            elif cmd.split()[0] == "disconnect_client":
                to_disconnect = cmd.split()[1]
                client_sock, addr = clients[to_disconnect]
                client_sock.send("DISCONNECTED_FROM_SERVER".encode())
                client_sock.close()
                print(f"Disconnected [{to_disconnect}] ({addr[0]}:{addr[1]})")
            elif cmd == "list_clients":
                for client in clients:
                    result = clients[client]
                    client_ip = result[1][0]
                    client_port = result[1][1]
                    print(f"\t[{client}] ({client_ip}:{client_port})")
            elif cmd.split()[0] == "send":
                client_name = cmd.split()[1]
                message: str = cmd.split()[2:]
                client_sock: socket.socket = clients[client_name][0]
                print("Sent", *message, "to", client_name)
                client_sock.send(*message.encode())
            else:
                print(f"Unknown command \"{cmd}\"")
        except:
            pass

def main():
    server_threads = []
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((SERVER_IP, SERVER_PORT))
    server_sock.listen(20)
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")
    print("Waiting for connections...")
    stop_server = threading.Event()
    clients = dict()
    processing_thread = threading.Thread(target=process_connections, args=(server_sock, server_threads, stop_server, clients))
    processing_thread.start()
    server_controls(stop_server, clients)
    processing_thread.join()

if __name__ == "__main__":
    main()