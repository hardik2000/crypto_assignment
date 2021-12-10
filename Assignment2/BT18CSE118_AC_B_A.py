"""
	HARDIK
	BT18CSE118
	$			 python BT18CSE118_AC_B_A.py localhost 8082

"""

import socket
import os
import sys
import re
import math
from Crypto.Random import new
from Crypto.Util.number import getPrime
from Crypto.Cipher import DES
import bitstring
from Crypto.Util.Padding import pad
from BT18CSE118_AC_B_Kg import *


def encode(pt, pk):
    e1 = pk[0]
    e2 = pk[1]
    p = pk[2]
    ct = {}
    ct["c1"] = []
    ct["c2"] = []
    r = random.randint(1, p)
    for s in pt:
        s_val = ord(s)
        c1 = pow_mod(e1, r, p)
        c2 = (pow_mod(e2, r, p) * s_val) % p
        ct["c1"].append(c1)
        ct["c2"].append(c2)
    return json.dumps(ct)


class Client:
    def __init__(self, server, port):
        # Create a Client Socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10)
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
        pk = json.loads(ack[1])
        print("Public key received is ", pk)
    except socket.timeout:
        print("!!!!SESSION TIMED OUT!!!!\n!!!!SERVER IS BUSY!!!!")
        os._exit(1)
    try:
        with open("BT18CSE118_AC_B_Msg.txt", "r") as f:
            lines = f.readlines()
        request = lines[0]
        try:
            print("Text send to server is ", request)
            request = encode(request, pk)
            ret = client.Request(request).decode("utf-8")
            if ret == "":
                print("Server Not Found \n")
                print("Client Connection Broken\n")
            print("Server replied : ", ret)
        except:
            print("Client Connection Broken\n")
            exit(1)
    except KeyboardInterrupt:
        print("\nClient Connection Broken\n")
        exit(1)

