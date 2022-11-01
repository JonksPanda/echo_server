from socket import *
from time import sleep
from threading import Thread, enumerate
import sys


class Client:
    def __init__(self) -> None:
        self.PORT = 54321
        self.HOST = "127.0.0.1"
        self.alive = True

    def close_connection(self, socket):
        print("Lost connection to server..")
        self.alive = False
        socket.close()
        sys.exit()

    def listen(self, s):
        while True:
            try:
                data = s.recv(1024)
                if not data:
                    self.close_connection(s)
                    break
                print(f"received '{data.decode()}'")
            except:
                self.close_connection(s)

    def send_message(self):
        try:
            self.alive = True
            with socket() as s:
                s.connect((self.HOST, self.PORT))
                listen = Thread(target=self.listen, args=(s,), daemon=True)
                listen.start()
                while True:
                    sleep(0.2)
                    message = input("message: ")
                    if not self.alive:
                        break
                    if message == "q":
                        sys.exit()
                    s.sendall(message.encode())

        except ConnectionRefusedError:
            print("Can't connect to server!")

    def connection_loop(self):
        while True:
            self.send_message()


def main():
    Client().connection_loop()


if __name__ == "__main__":
    main()
