#coding=utf-8
import re, socket

domain = []
ip = []
version = []

with open('inputfile.txt', 'r') as f:
    for line in f.readlines():
        if re.match(r'\d+.\d+.\d+.\d+', line):
            host = socket.gethostbyaddr(line.strip('\n'))
            domain.append(host[0])
            ip.append(line.strip('\n'))
        else:
            host = socket.getaddrinfo(line.strip('\n'), 'http')
            domain.append(line.strip('\n'))
            ip.append(host[0][4][0])
f.close()

for i in ip:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((i,22))
    s = sock.recv(1024).decode("utf-8")
    version.append(s)
    sock.close()

print({'domain':domain, 'ip':ip, 'version-version':version})
