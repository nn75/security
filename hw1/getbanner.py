import sys
import socket


def send_quit(hostname, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    s.connect((hostname, port))
    s.send("QUIT\n".encode())

    old_len = 0
    data = ""
    while True:
        try:
            data += s.recv(4096).decode()
        except socket.timeout:
            break
        else:
            if len(data) == old_len:
                break
            else:
                old_len = len(data)
    s.close()
    return data


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./nn.py <hostname> <port>")
        exit(-1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])

    print(send_quit(hostname, port),end="")
