"""
    HARDIK
    BT18CSE118
    $           python BT18CSE118_EA_B_A.py localhost 8082

"""

import socket
import os
import sys
from _thread import *
import threading
import random
from BT18CSE118_EA_B_Kg import *


def Alice(S, n, request, clientAddress):
    S = int(S)
    n = int(n)
    while True:
        r = random.randint(0, n - 1)
        print("\nRandom r value generated is", r)
        x = (r * r) % n
        print("x value generated is", x)
        try:
            request.send(str(x).encode("utf-8"))
        except:
            print("Connection Closed ")
            request.close()
            break
        try:
            c = request.recv(1024).decode("utf-8")
        except:
            request.close()
            break
        print("C Received from is : ", int(c))

        try:
            c = int(c)
            if c == 1:
                y = (r * S) % n
            else:
                y = r % n
            print("Response y is : ", y)
            request.send(str(y).encode("utf-8"))
        except KeyboardInterrupt:
            print("Connection Closed ")
            request.close()
            break


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

            """
                Reading keys from the file
            """
            S, V, n = key_read()
            print("S ", S, " V ", V, " n ", n)
            # Acknoledge the Connection
            ack = "Connection established\n" + V + "\n" + n
            request.send(ack.encode("utf-8"))

            try:
                Alice(S, n, request, clientAddress)
            except Exception as e:
                print("Connection Closed ", e)
                request.close()
        except Exception as e:
            print("2Connection Closed ", e)
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
