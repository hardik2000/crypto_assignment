"""
    HARDIK
    BT18CSE118
    $           python BT18CSE118_SE_B_De.py localhost 8082

"""

import socket
import os
import sys
from _thread import *
import threading
from Crypto.Cipher import DES
import bitstring
from Crypto.Util.Padding import pad


def key_read():
    with open("BT18CSE118_SE_B_Sk.txt", "rb") as f:
        lines = f.readlines()
    key = lines[0]
    IV = lines[1]
    return key[:-1], IV


def xor_fun(a, b):
    c = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            c += "0"
        else:
            c += "1"
    return c


def bit_to_byte(s):
    i = 0
    r = ""
    while i < len(s):
        x = s[i : i + 8]
        i += 8
        r += chr(int(x, 2))
    return r.encode()


def decode(ct, sk1, IV):
    block_size = 16
    IV_size = 32
    pt = ""
    i = 0
    cipher = DES.new(sk1, DES.MODE_ECB)
    n = len(IV) % 8
    IV = IV + (b" " * n)
    n_bit_ct = cipher.encrypt(IV)
    n_bit_ct = int.from_bytes(n_bit_ct, byteorder=sys.byteorder)
    n_bit_ct = format(n_bit_ct, "b").zfill((IV_size * 8))[: (block_size * 8)]
    vars = ct[0:block_size]
    i += block_size
    ci = ""
    while len(vars) < block_size:
        vars += " "
    for var in vars:
        ci += str(format(ord(var), "b").zfill(8))[:8]

    pi = xor_fun(ci, n_bit_ct)
    pt += pi

    while i < len(ct):
        IV = int.from_bytes(IV, byteorder=sys.byteorder)
        IV = format(IV, "b").zfill((IV_size * 8))
        IV = IV[(block_size * 8) :] + ci
        IV = bit_to_byte(IV)
        n = len(IV) % 8
        IV = IV + (b" " * n)
        n_bit_ct = cipher.encrypt(pad(IV, IV_size))
        n_bit_ct = int.from_bytes(n_bit_ct, byteorder=sys.byteorder)
        n_bit_ct = format(n_bit_ct, "b").zfill((IV_size * 8))[: (block_size * 8)]
        vars = ct[i : i + block_size]
        i += block_size
        ci = ""
        while len(vars) < block_size:
            vars += " "
        for var in vars:
            ci += str(format(ord(var), "b").zfill(8))[:8]

        pi = xor_fun(ci, n_bit_ct)
        pt += pi
    i = 0
    new_pt = ""
    while i < len(pt):
        x = int(pt[i : i + 8], 2)
        new_pt += chr(x)
        i += 8
    return new_pt.strip()


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
                msg = request.recv(1024).decode("utf-8")
                if not msg:
                    print("Connection Closed ")
                    request.close()
                    os._exit(1)
                print("\nCipher Text Received from (", clientAddress, ") is : \n", msg)

                try:
                    print()
                    # evaluate the msgression and send the output
                    ret = decode(msg, sk1, sk2)
                    print(
                        "\nPlain Text Received from (", clientAddress, ") is : \n", ret
                    )
                    request.send(ret.encode("utf-8"))
                except Exception as e:
                    print("Connection Closed", e)
                    request.close()
            except Exception as e:
                print("Connection Closed", e)
                request.close()
        except Exception as e:
            print("Connection Closed", e)
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
