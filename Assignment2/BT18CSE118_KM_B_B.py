"""
	HARDIK
	BT18CSE118
	$			 python BT18CSE118_KM_B_B.py localhost 8082

"""

import socket
import os
import sys
from Crypto.Random import new
from Crypto.Util.number import getPrime
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import json
from Crypto.Cipher import DES
import random


def key_read():
    with open("BT18CSE118_KM_B_BSk.txt", "rb") as f:
        KB = f.readlines()[0]
    return KB


def decode_msg_from_alice(ticket_for_bob):
    KB = key_read()
    cipher = DES.new(KB, DES.MODE_CFB)
    try:
        ticket_for_bob = cipher.decrypt(ticket_for_bob)
    except Exception as e:
        print(e)
        exit(1)
    ticket_for_bob = ticket_for_bob[16:]
    print("Ticket received from Alice ", ticket_for_bob)
    ticket_for_bob = json.loads(ticket_for_bob)
    print("Got connection request from ", ticket_for_bob["fro"])
    return ticket_for_bob["KAB"].encode("ISO-8859-1")


def encode_rb_for_alice(KAB, RB):
    cipher = DES.new(KAB, DES.MODE_CFB)
    exp = cipher.encrypt(("    " + str(RB)).encode("UTF-16"))
    return exp


def decode_rb_from_alice(ret, KAB, RB):
    cipher = DES.new(KAB, DES.MODE_CFB)
    ret = cipher.decrypt(ret)
    ret = ret.decode("UTF-16")[4:]
    print("RB received from bob is ", ret)
    if int(ret) == (int(RB) - 1):
        print("YES ACCEPTED THAT NOW ALICE CAN COMMUNICATE")
    else:
        print("NO ALICE CAN COMMUNICATE")


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
        self.socket.send(request.encode("ISO-8859-1"))
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
        ack = client.socket.recv(4096).decode("ISO-8859-1")
        ack = ack.split("\n")
        print(ack[0])
        ticket_for_bob = ack[1].encode("ISO-8859-1")
        print("Ticket received for Alice is ", ticket_for_bob)
    except socket.timeout:
        print("!!!!SESSION TIMED OUT!!!!\n!!!!SERVER IS BUSY!!!!")
        os._exit(1)
    try:
        try:
            KAB = decode_msg_from_alice(ticket_for_bob)
            RB = random.getrandbits(16)  # no of bits=16
            print("RB generated is ", RB)
            request = encode_rb_for_alice(KAB, RB)
            client.socket.send(request)
            ret = client.socket.recv(1024)
            decode_rb_from_alice(ret, KAB, RB)
            print("-" * 20 + "END" + "-" * 20)
        except:
            print("Client Connection Broken\n")
            exit(1)
    except KeyboardInterrupt:
        print("\nClient Connection Broken\n")
        exit(1)
    finally:
        exit(1)
