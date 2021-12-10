"""
    HARDIK
    BT18CSE118
    $           python BT18CSE118_SE_Z_De.py localhost 8082

"""

import socket
import os
import sys
from _thread import *
import threading


def key_read():
    with open("BT18CSE118_SE_Z_Sk.txt", "r") as f:
        lines = f.readlines()
    sk1, sk2 = lines[0].split(" ")
    return sk1, sk2


def xor_fun(a, b):
    c = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            c += "0"
        else:
            c += "1"
    return c


"""
Eg:
    Roll No -> 1 8
            10010[:-1] -> 1001
        Taking 1 and 1    
"""


def f_fun(a, b):
    r_no = "18"
    r_no = str(format(int(r_no), "b").zfill(5))[:4]
    b = r_no[:1] + b[1:3] + r_no[-1:]
    return xor_fun(a, b)


def decode(ct, sk1, sk2):
    sk1 = str(format(int(sk1), "b").zfill(4))[:4]
    sk2 = str(format(int(sk2), "b").zfill(4))[:4]
    pt = ""
    ct = ct.strip()
    for i in ct:
        val = str(format(ord(i), "b").zfill(8))[:8]
        L4, R4 = val[:4], val[4:]
        L5, R5 = xor_fun(R4, f_fun(L4, sk2)), L4
        L6, R6 = xor_fun(R5, f_fun(L5, sk1)), L5
        pt += chr(int(L6 + R6, 2))
    return pt


class Server:
    def __init__(self, hostname, port):
        # created a server socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        """
            the SO_REUSEADDR flag tells the kernel to
            reuse a local socket in TIME_WAIT state,
            without waiting for its natural timeout to expire.
        """

        # Bind the socket to specified hostname and port
        self.sock.bind((hostname, port))

        # Listen to 1 client at a time
        self.sock.listen(1)

    def listenToClient(self):
        try:
            request, clientAddress = self.sock.accept()

            # Client Information
            print("Received a request from : ", clientAddress)
            # Acknoledge the Connection
            ack = "\nConnection established\n"
            request.send(ack.encode("utf-8"))

            try:
                sk1, sk2 = key_read()
                print("Secret Key 1 ", sk1)
                print("Secret Key 2 ", sk2)

                msg = request.recv(1024).decode("utf-8")
                print("Cipher Text Received is : ", msg)

                try:
                    ret = decode(msg, sk1, sk2)
                    print("Plain Text Received is : ", ret)
                    request.send(ret.encode("utf-8"))
                except Exception as e:
                    print("Connection Closed ", e)
                    request.close()
            except Exception as e:
                print("Connection Closed ", e)
                request.close()
        except Exception as e:
            print("Connection Closed ", e)
            request.close()


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
    print("Server established----->( %s on port :%s )" % (hostname, port))
    # Run Server
    server.listenToClient()
