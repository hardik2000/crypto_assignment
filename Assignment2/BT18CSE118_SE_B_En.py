"""
	HARDIK
	BT18CSE118
	$			 python BT18CSE118_SE_B_En.py localhost 8082

"""

import socket
import os
import sys
from Crypto.Random import new
from Crypto.Util.number import getPrime
from Crypto.Cipher import DES
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


def encode(pt, sk1, IV):
    block_size = 16
    IV_size = 32
    ct = ""
    i = 0
    cipher = DES.new(sk1, DES.MODE_ECB)
    n = len(IV) % 8
    IV = IV + (b" " * n)
    n_bit_ct = cipher.encrypt(IV)
    n_bit_ct = int.from_bytes(n_bit_ct, byteorder=sys.byteorder)
    n_bit_ct = format(n_bit_ct, "b").zfill((IV_size * 8))[: (block_size * 8)]
    vars = pt[0:block_size]
    i += block_size
    pi = ""
    while len(vars) < block_size:
        vars += " "
    for var in vars:
        x = str(format(ord(var), "b").zfill(8))
        pi += x[:8]

    ci = xor_fun(pi, n_bit_ct)
    ct += ci
    while i < len(pt):
        IV = int.from_bytes(IV, byteorder=sys.byteorder)
        IV = format(IV, "b").zfill((IV_size * 8))
        IV = IV[(block_size * 8) :] + ci
        IV = bit_to_byte(IV)
        n = len(IV) % 8
        IV = IV + (b" " * n)
        n_bit_ct = cipher.encrypt(pad(IV, IV_size))
        n_bit_ct = int.from_bytes(n_bit_ct, byteorder=sys.byteorder)
        n_bit_ct = format(n_bit_ct, "b").zfill((IV_size * 8))[: (block_size * 8)]
        vars = pt[i : i + block_size]
        i += block_size
        pi = ""
        while len(vars) < block_size:
            vars += " "
        for var in vars:
            pi += str(format(ord(var), "b").zfill(8))[:8]

        ci = xor_fun(pi, n_bit_ct)
        ct += ci
    i = 0
    new_ct = ""
    while i < len(ct):
        x = int(ct[i : i + 8], 2)
        new_ct += chr(x)
        i += 8
    return new_ct


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
        print(client.socket.recv(1024).decode("utf-8"))
    except socket.timeout:
        print("!!!!SESSION TIMED OUT!!!!\n!!!!SERVER IS BUSY!!!!")
        os._exit(1)
    try:
        sk1, IV = key_read()
        print("Secret Key ", sk1)
        print("IV ", IV)
        with open("BT18CSE118_SE_B_Msg.txt", "r") as f:
            lines = f.readlines()
        request = lines[0]
        print("Message sent is ", request)
        if request == "quit":
            client.socket.close()
            print("Client Connection  Closed\n")
            exit(0)
        try:
            # request = re.sub(r"[^\w\s]", "", request)
            request = encode(request, sk1, IV)
            ret = client.Request(request).decode("utf-8")
            if ret == "":
                print("Server Not Found \n")
                print("Client Connection Broken\n")
            print("Server replied : ", ret)
            client.socket.close()
        except:
            print("Client Connection Broken\n")
            client.socket.close()
            exit(1)

    except KeyboardInterrupt:
        print("\nClient Connection Broken\n")
        client.socket.close()
        exit(1)

