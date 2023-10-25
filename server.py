import socket
import argparse
import sys
import json
import threading
import time
from _thread import *




def broadcast_message(message, sender, clients):
    for connection in clients:
        if connection != sender:
            try:
                connection.send(message.encode("utf-8"))
            except:
                connection.close()
                clients.remove(connection)



def client_thread(client_socket, client_address,server_ip, port, server_passcode, clients, lock):
    new_user = True

    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8")

        if request and not new_user:
            print(f"{request}")
            sys.stdout.flush()
            broadcast_message(request, client_socket, clients)



        if new_user:
            clients.append(client_socket)
            lst = json.loads(request)
            username = lst[0]
            pw = lst[1]
            if pw == server_passcode:
                print(f"{username} joined the chatroom")
                sys.stdout.flush()
                broadcast_message(f"{username} joined the chatroom", client_socket, clients)
                response = f"Connected to {server_ip} on port {port}".encode("utf-8")
                client_socket.send(response)
                new_user = False
            else:
                response = f"Incorrect passcode".encode("utf-8")
                client_socket.send(response)
                client_socket.close()
                with lock:
                    clients.remove(client_socket)


    client_socket.close()





def create_socket():
    #create a server using python3 server.py -start -port <port> -passcode <passcode>


    server_ip = "127.0.0.1"



    #TCP socket server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    parser = argparse.ArgumentParser()

    #arg to start server
    parser.add_argument('-start', '--start', action='store_true')
    #define port number
    parser.add_argument('-port', '--port', help="Enter port number")
    #define passcode
    parser.add_argument('-passcode', '--passcode', help="Enter passcode")
    #parse command line arguments
    args = parser.parse_args()
    lock = threading.Lock()

    # Command-line arguments
    port = int(args.port)
    server_passcode = args.passcode


    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, port))
        server_socket.listen(0)
        print(f"Server started on port {port}. Accepting connections")
        sys.stdout.flush()
    except Exception as e:
        print(f"Error: {e}")
        return

    clients = []

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=client_thread, args=(client_socket, client_address, server_ip, port, server_passcode, clients, lock)).start()

    server_socket.close()





if __name__ == '__main__':
    create_socket()