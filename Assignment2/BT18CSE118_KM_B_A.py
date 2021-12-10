"""
	HARDIK
	BT18CSE118
	$			 python BT18CSE118_KM_B_A.py localhost 8082

"""

import socket
import sys
import random
from Crypto.Cipher import DES
import json


def key_read():
    with open("BT18CSE118_KM_B_ASk.txt", "rb") as f:
        KA = f.readlines()[0]
    return KA


def decode_msg_from_kdc(exp, RA):
    KA = key_read()
    cipher = DES.new(KA, DES.MODE_CFB)
    exp = cipher.decrypt(exp)
    exp = exp.decode("ISO-8859-1")
    exp = exp[16:]
    try:
        exp = json.loads(exp)
    except Exception as e:
        print(e)
    if RA != int(exp["RA"]):
        print("MATCH NOT FOUND")
        raise Exception("Sorry, RA match not found hence terminating")
    else:
        print("RA MATCH FOUND")
    return exp["KAB"].encode("ISO-8859-1"), exp["ticket_for_bob"].encode("ISO-8859-1")


def decode_msg_from_bob(exp, KAB):
    cipher = DES.new(KAB, DES.MODE_CFB)
    exp = cipher.decrypt(exp)
    exp = exp.decode("UTF-16")[4:]
    print("RB value received is ", exp)
    cipher = DES.new(KAB, DES.MODE_CFB)
    x = ("    " + str(int(exp) - 1)).encode("UTF-16")
    exp = cipher.encrypt(x)
    return exp


class Server:
    def __init__(self, hostname, port):
        # created a server socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to specified hostname and port
        self.sock.bind((hostname, port))
        # Listen to 1 client at a time
        self.sock.listen(1)

    def listenToClient(self):
        KAB = None
        ticket_for_bob = None
        # conversation with KDC to get KAB
        try:
            request, clientAddress = self.sock.accept()
            # Client Information
            print("Received a request from : ", clientAddress)
            # Acknoledge the Connection
            RA = random.getrandbits(16)  # no of bits=16
            print("RA generated is ", RA)
            ack = "Connection established\nAlice Bob " + str(RA)
            request.send(ack.encode("ISO-8859-1"))
            try:
                # receive the expression
                exp = request.recv(4096)
                # print(exp)
                KAB, ticket_for_bob = decode_msg_from_kdc(exp, RA)
            except Exception as e:
                print("Connection Closed - ", e)
                request.close()
                exit(1)
        except Exception as e:
            print("Connection Closed - ", e)
            try:
                request.close()
            except UnboundLocalError:
                print("UnboundLocalError Caught")
            self.sock.close()
            exit(1)
        print("KAB", KAB)
        print("ticket_for_bob", ticket_for_bob)
        if KAB != None and ticket_for_bob != None:
            # conversation with BOB to confirm authenticity
            try:
                request, clientAddress = self.sock.accept()
                # Client Information
                print("Received a request from : ", clientAddress)
                # Acknoledge the Connection
                ack = "Connection established\n" + ticket_for_bob.decode("ISO-8859-1")
                request.send(ack.encode("ISO-8859-1"))
                try:
                    # receive the expression
                    ret = request.recv(1024)
                    print("msg received from bob is ", ret)
                    ret = decode_msg_from_bob(ret, KAB)
                    request.send(ret)
                except Exception as e:
                    print("Connection Closed - ", e)
                    request.close()
            except Exception as e:
                print("Connection Closed - ", e)
                try:
                    request.close()
                except UnboundLocalError:
                    print("UnboundLocalError Caught")
                self.sock.close()
                exit(1)
        else:
            print("Error")
            self.sock.close()
            exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage : %s [hostname] [port number]" % sys.argv[0])
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])

    try:
        # Create Server
        server = Server(hostname, port)
    except:
        print("Server Not Created\n")
        sys.exit(1)
    print("Server established----->( %s on port :%s )\n" % (hostname, port))
    # Run Server
    server.listenToClient()

