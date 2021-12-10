"""
	HARDIK
	BT18CSE118
	$			 python BT18CSE118_EA_B_B.py localhost 8082

"""

import socket
import os
import sys
from Crypto.Random import new
from Crypto.Util.number import getPrime
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from BT18CSE118_EA_B_Kg import *


def Bob(V, n, client):
    try:
        satisfied = True
        for i in range(5):
            print("Round ", i + 1)
            x = int(client.socket.recv(1024).decode("utf-8"))
            print("x value received is ", x)

            try:
                c = random.randint(0, 1)
                try:
                    print("C value is : ", c)
                    y = int(client.Request(str(c)).decode("utf-8"))
                    print("Response y received : ", y)
                    lhs = (y * y) % n
                    if c == 1:
                        rhs = (V * x) % n
                    else:
                        rhs = (x) % n
                    print("LHS = ", lhs, "RHS = ", rhs)
                    if lhs != rhs:
                        satisfied = False
                        break
                except Exception as e:
                    print("Client Connection Broken -> ", e)
                    client.socket.close()
                    exit(1)
            except KeyboardInterrupt:
                print("\nClient Connection Broken\n")
                client.socket.close()
                exit(1)
        if satisfied:
            print("\nYes fully satisfied that user is Alice")
            client.socket.close()
        else:
            print("\nNo user is not Alice")
            client.socket.close()
    except Exception as e:
        print(e)
        client.socket.close()


class Client:
    def __init__(self, server, port):
        # Create a Client Socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.settimeout(60)
        # Bind the socket to specified hostname and port
        self.socket.connect((server, port))

    def Request(self, request):
        if request == "":
            request = ""
        elif request[-1] != "\n":
            request += "\r\n"
        # Send Request
        self.socket.send(request.encode("utf-8"))
        # Retreive response
        return self.socket.recv(1024)

    def code(self):
        self.socket.send("\r\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Required: %s [host] [sever port]" % sys.argv[0])
        sys.exit(1)
    hostname = sys.argv[1]
    port = int(sys.argv[2])

    try:
        # Initiate Client
        client = Client(hostname, port)
    except:
        print("Client Connection not established\n")
        sys.exit(1)

    try:
        ack = client.socket.recv(1024).decode("utf-8")
        ack = ack.split("\n")
        print(ack[0])
        V = int(ack[1])
        n = int(ack[2])
        print("V value received is ", V)
        print("n value received is ", n)

        Bob(V, n, client)
    except socket.timeout:
        print("!!!!SESSION TIMED OUT!!!!\n!!!!SERVER IS BUSY!!!!")
        client.socket.close()
        os._exit(1)
