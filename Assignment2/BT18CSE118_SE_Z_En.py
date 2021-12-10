"""
	HARDIK
	BT18CSE118
	$			 python BT18CSE118_SE_Z_En.py localhost 8082

"""

import socket
import os
import sys
import re


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
    r_no = str(format(int(r_no), "b").zfill(5))[0:4]
    b = r_no[:1] + b[1:3] + r_no[-1:]
    return xor_fun(a, b)


def encode(pt, sk1, sk2):
    sk1 = str(format(int(sk1), "b").zfill(4))[:4]
    sk2 = str(format(int(sk2), "b").zfill(4))[:4]
    ct = ""
    for x in pt:
        bin_str = str(format(ord(x), "b").zfill(8))[:8]
        L1, R1 = bin_str[:4], bin_str[4:]
        L2, R2 = R1, xor_fun(L1, f_fun(R1, sk1))
        L3, R3 = R2, xor_fun(L2, f_fun(R2, sk2))
        ct += chr(int(L3 + R3, 2))
    return ct


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
        sk1, sk2 = key_read()
        print("Secret Key 1 ", sk1)
        print("Secret Key 2 ", sk2)
        with open("BT18CSE118_SE_Z_Msg.txt", "r") as f:
            lines = f.readlines()
        request = lines[0]

        try:
            # request = re.sub(r"[^\w\s]", "", request)
            print("Message to be encrypted is ", request)
            request = encode(request, sk1, sk2)
            ret = client.Request(request).decode("utf-8")
            if ret == "":
                print("Server Not Found \n")
                print("Client Connection Broken\n")
            print("Server replied : ", ret)
        except Exception as e:
            print("Client Connection Broken\n")
            client.socket.close()
            exit(1)
    except Exception as e:
        print("\nClient Connection Broken\n")
        client.socket.close()
        exit(1)

