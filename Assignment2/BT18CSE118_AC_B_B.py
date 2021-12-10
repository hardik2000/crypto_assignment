"""
    HARDIK
    BT18CSE118
    $           python BT18CSE118_AC_B_B.py localhost 8082

"""

import json
import socket
import os
import sys
from Crypto.Util.Padding import pad
from BT18CSE118_AC_B_Kg import *

# extended euclidean algoroithm
def extended_euclidean(a, b):
    if b == 0:
        return a, 1, 0
    x2 = 1
    x1 = 0
    y2 = 0
    y1 = 1

    # algorithm as per book 2.107
    while b > 0:
        q = a // b
        r = a - q * b
        x = x2 - q * x1
        y = y2 - q * y1
        a = b
        b = r
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y
    return a, x2, y2


# function to calculate multiplicative inverse
def inv_fun(a, b):
    g, x, y = extended_euclidean(a, b)
    res = (x % b + b) % b
    return res


def decode(ct, sk):
    d = sk[0]
    p = sk[1]
    ct = json.loads(ct)
    pt = ""
    for i in range(len(ct["c1"])):
        c1 = ct["c1"][i]
        c2 = ct["c2"][i]
        pt += chr((c2 * inv_fun(pow_mod(c1, d, p), p)) % p)
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

            """
                Reading keys from the file
            """
            keys = key_read()
            pk = keys["pk"]
            sk = keys["sk"]
            print("Secret Key is ", sk, "\nPublic key is ", pk)
            # Acknoledge the Connection
            ack = "Connection established\n" + json.dumps(pk)
            request.send(ack.encode("utf-8"))

            try:
                msg = request.recv(1024).decode("utf-8")
                if not msg:
                    print("Connection Closed  from ", clientAddress)
                    request.close()
                    os._exit(1)
                print("\nCipher Text Received from (", clientAddress, ") is : \n", msg)

                try:
                    print()
                    # evaluate the msgression and send the output
                    ret = decode(msg, sk)
                    print(
                        "\nPlain Text Received from (", clientAddress, ") is : \n", ret
                    )
                    request.send(ret.encode("utf-8"))
                    sys.exit(1)
                except Exception as e:
                    print("Connection Closed ", e)
                    request.close()
                    sys.exit(1)
            except Exception as e:
                print("Connection Closed ", e)
                request.close()
                sys.exit(1)
        except Exception as e:
            print("Connection Closed ", e)
            request.close()
            sys.exit(1)


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
    server.listenToClient()
