import socket
import argparse
import sys




def run_client():

    # create a socket client to connect to TCP server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #server's IP address
    server_ip = "127.0.0.1"

    parser = argparse.ArgumentParser()

    #indicate client is joining the server
    parser.add_argument('-join', '--join', action='store_true')
    #host number
    parser.add_argument('-host', '--host', help="Enter host number")
    #port number
    parser.add_argument('-port', '--port', help="Enter port number")
    #client username for chatroom
    parser.add_argument('-username', '--username', help="Enter username")
    #password for the server
    parser.add_argument('-passcode', '--passcode', help="Enter passcode")

    args = parser.parse_args()

    username = args.username
    passcode = args.passcode
    #ensure port is an integer
    server_port = int(args.port)

    #connect to TCP server
    client.connect((server_ip, server_port))


    client.close()



run_client()