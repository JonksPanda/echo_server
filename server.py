from socket import *
from time import sleep
from threading import Thread, enumerate
import sys
import os


class Server:
    def __init__(self) -> None:
        self.HOST = "127.0.0.1"
        self.PORT = 54321
        self.threads = enumerate()
        self.connections = {}

    def close_connection(self, addr):
        for thread in self.threads:
            name = thread.name
            if str(name) == str(addr):
                print(f"closing connection {addr}")
                self.connections[addr].close()
                self.connections.pop(addr, None)
                sys.exit()

    def self_destruct(self, addr):
        print(f"{addr} initiated self destruct..")
        for addr in self.connections.keys:
            print(addr)
            self.close_connection(addr)

    def connect(self, conn, addr):
        while True:
            print(self.threads)
            with conn:
                print("connected by", addr)
                while True:
                    try:
                        data = conn.recv(1024)
                        print(f"received from {addr}: {data.decode()}")
                        if not data:
                            self.close_connection(addr)
                            break
                        data = self.check_command(data.decode(), conn, addr)
                    except:
                        self.close_connection(addr)
                        break

    def send_message(self, msg, conn):
        conn.sendall(msg.encode())

    def repeat(self, string, times, conn):
        string = f"repeat: {string}"
        if int(times) < 1:
            self.send_message(string, conn)
        else:
            for i in range(int(times)):
                sleep(0.01)
                self.send_message(string, conn)

    def reverse_string(self, string):
        return string[::-1]

    def check_command(self, string, conn, addr):
        command = string[0:1:].lower()
        if command == "u":
            self.send_message(f"upper: {string[1:].upper()}", conn)
        elif command == "r":
            self.send_message(
                f"reverse: {self.reverse_string(string[1:])}", conn)
        elif command == "b":
            self.broadcast(f"broadcast: {string[1:]}", addr)
        elif string.lower() == "self destruct":
            self.self_destruct(addr)
        elif command.isnumeric():
            self.repeat(string[1:], command, conn)
        else:
            self.send_message(string, conn)

    def connection_loop(self):
        with socket() as s:
            s.bind((self.HOST, self.PORT))
            while True:
                s.listen(1)
                conn, addr = s.accept()
                self.connections.update({addr: conn})
                self.threads.append(
                    Thread(target=self.connect, args=(conn, addr), daemon=True, name=addr))
                self.threads[-1].start()

    def broadcast(self, string, addr):
        for conn in self.connections.values():
            self.send_message(f"from {addr}: {string}", conn)


def main():
    server = Server()
    server.connection_loop()
    server.threads


if __name__ == "__main__":
    main()
