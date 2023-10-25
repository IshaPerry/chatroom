import socket
import argparse
import sys





clients = []



def create_socket():
    #create a server using python3 server.py -start -port <port> -passcode <passcode>
    #set initial port and passcode with this command
    global port
    global server_passcode
    global server_ip

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


    port = int(args.port)
    server_passcode = args.passcode
    #bind server
    server.bind((server_ip, port))
    #listen for potential clients
    server.listen(0)

    print(f"Server started on port {port}. Accepting connections")
    sys.stdout.flush()


    server.close()

create_socket()


