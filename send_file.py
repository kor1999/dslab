import socket
import time
import sys
import os

file, addr, port = sys.argv[1], sys.argv[2], int(sys.argv[3])

s = socket.socket()
s.connect((addr,port))

f = open (file, "rb")
encoded_file = bytes(file, 'utf-8')

b = bytearray()
for i in range(100 - len(encoded_file)):
    b.append(0)

b += encoded_file
s.send(b)


size_of_file = os.path.getsize(file)

sent = 0

l = f.read(1024)
while (l):
    s.send(l)
    l = f.read(1024)
    print('Sent: ' + str((sent * 100/size_of_file)) + '%')
    sent += 1024
    
s.close()
