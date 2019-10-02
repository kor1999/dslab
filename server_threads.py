import socket
import random
import os
from threading import Thread


clients = []


# Thread to listen one particular client
class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name

    # clean up
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        while True:
            # try to read 1024 bytes from user
            # this is blocking call, thread will be paused here


            file_bytes = bytearray(self.sock.recv(100))
            while file_bytes[0] == 0:
                file_bytes.remove(0)

            file_name = file_bytes.decode('utf-8')

            if os.path.exists(file_name):
                extension = file_name[file_name.rfind('.') + 1:]
                file_name = file_name[:file_name.rfind('.')]
                file_name += str(random.randint(0, 1000)) + '.' + extension
            
            print('kek: ', file_name)

            f = open(file_name, 'wb+')
            
            data = self.sock.recv(1024)
            while (data):
                f.write(data)
                data = self.sock.recv(1024)

            f.close()
            # if we got no data – client has disconnected
            self._close()
            # finish the thread
            return


def main():
    next_name = 1

    # AF_INET – IPv4, SOCK_STREAM – TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse address; in OS address will be reserved after app closed for a while
    # so if we close and imidiatly start server again – we'll get error
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # listen to all interfaces at 8800 port
    sock.bind(('', 8800))
    sock.listen()
    while True:
        # blocking call, waiting for new client to connect
        con, addr = sock.accept()
        clients.append(con)
        name = 'u' + str(next_name)
        next_name += 1
        print(str(addr) + ' connected as ' + name)
        # start new thread to deal with client
        ClientListener(name, con).start()


if __name__ == "__main__":
    main()
