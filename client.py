from socket import *
from time import sleep
from threading import Thread, enumerate


class Client:
    def __init__(self) -> None:
        self.PORT = 54321
        self.HOST = "127.0.0.1"

    def listen(self, s):
        while True:
            data = s.recv(1024)
            # if not data:
            #     break
            print(f"received '{data.decode()}'")

    def send_message(self):
        try:
            with socket() as s:
                s.connect((self.HOST, self.PORT))
                Thread(target=self.listen, args=(s,), daemon=False).start()
                while True:
                    print(enumerate())
                    message = input("message: ")
                    s.sendall(message.encode())
                    sleep(0.01)

        except ConnectionRefusedError:
            print("Can't connect to server!")

    def connection_loop(self):
        while True:
            self.send_message()


def main():
    Client().connection_loop()


if __name__ == "__main__":
    main()
