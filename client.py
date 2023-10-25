import socket
import argparse
import sys
import json
import threading
import time
from _thread import *
from datetime import datetime, timedelta



def receive_messages(client, username):
        #receieve message while responses are sent
        while True:
            response = client.recv(1024).decode("utf-8")
            while response:
                print(response)
                sys.stdout.flush()
                response = client.recv(1024).decode("utf-8")

def send_messages(client, username):
        while True:
        # input message and send it to the server
            try:
                #send any messafe
                msg = input("")
                #shortcut to send feeling happy
                if msg == ":)":
                    msg = "[feeling happy]"
                    newmsg = username + ": " + msg
                #shortcut to send feeling sad
                elif msg == ":(":
                    msg = "[feeling sad]"
                    newmsg = username + ": " + msg
                #shortcut to send time
                elif msg == ":mytime":
                    msg = time.strftime("%H:%M:%S")
                    newmsg = username + ": " + msg
                    # msg = time.time()
                #shortcut to exit chatroom
                elif msg == ":Exit":
                    newmsg = username + " left the chatroom"
                #shortcut to add 1 hr to current time
                elif msg == ":+1hr":
                    current_time = datetime.now()
                    new_time = current_time + timedelta(hours=1)
                    newmsg = username + ": " + new_time.strftime("%H:%M:%S")
                else:
                    newmsg = username + ": " + msg
                client.send(newmsg.encode("utf-8")[:1024])
            except:
                sys.exit(1)


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

    #create username and password to send to server for new client
    lst = [username, passcode]
    lst = json.dumps(lst)
    client.send(lst.encode())
    sent = True
    response = client.recv(1024)
    response = response.decode("utf-8")
    if sent:
        sent = False


    #threading to allow clients to send and recieve messages at same time
    send_thread = threading.Thread(target=send_messages, args=(client, username))
    receive_thread = threading.Thread(target=receive_messages, args=(client, username))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    client.close()
    print("Connection to server closed")
    sys.stdout.flush()


run_client()