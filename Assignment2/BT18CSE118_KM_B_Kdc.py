"""
	HARDIK
	BT18CSE118
	$			 python BT18CSE118_KM_B_Kdc.py localhost 8082

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


def key_read():
    with open("BT18CSE118_KM_B_ASk.txt", "rb") as f:
        KA = f.readlines()[0]
    with open("BT18CSE118_KM_B_BSk.txt", "rb") as f:
        KB = f.readlines()[0]
    return KA, KB


def encode_msg_for_alice(fro, to, RA):
    print("From ", fro, " To ", to, " RA ", RA)
    KA, KB = key_read()
    KAB = get_random_bytes(8)

    ticket_for_bob = {}
    ticket_for_bob["fro"] = fro
    ticket_for_bob["KAB"] = KAB.decode("ISO-8859-1")
    print("Ticket for Bob ", ticket_for_bob)
    ticket_for_bob = json.dumps(ticket_for_bob)
    ticket_for_bob = "                " + ticket_for_bob
    cipher = DES.new(KB, DES.MODE_CFB)
    try:
        ticket_for_bob = cipher.encrypt(ticket_for_bob.encode("ISO-8859-1"))
    except Exception as e:
        print(e)
        exit(1)

    msg_for_alice = {}
    msg_for_alice["RA"] = RA
    msg_for_alice["to"] = to
    msg_for_alice["KAB"] = KAB.decode("ISO-8859-1")
    try:
        msg_for_alice["ticket_for_bob"] = ticket_for_bob.decode("ISO-8859-1")
    except Exception as e:
        print(e)
        exit(1)
    print("Msg for Alice ", msg_for_alice)
    try:
        msg_for_alice = json.dumps(msg_for_alice)
    except Exception as e:
        print(e)
        exit(1)
    msg_for_alice = "                " + msg_for_alice

    try:
        cipher = DES.new(KA, DES.MODE_CFB)
        msg_for_alice = cipher.encrypt(msg_for_alice.encode("ISO-8859-1"))
    except Exception as e:
        print(e)
        exit(1)
    return msg_for_alice


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
        fro, to, RA = ack[1].split(" ")
    except socket.timeout:
        print("!!!!SESSION TIMED OUT!!!!\n!!!!SERVER IS BUSY!!!!")
        os._exit(1)
    try:
        try:
            request = encode_msg_for_alice(fro, to, RA)
            ret = client.socket.send(request)
            if ret == "":
                print("Server Not Found \n")
                print("Client Connection Broken\n")
                exit(1)
            print("Transmission Successful")
        except:
            print("Client Connection Broken\n")
            exit(1)
    except KeyboardInterrupt:
        print("\nClient Connection Broken\n")
        exit(1)
    finally:
        exit(1)
