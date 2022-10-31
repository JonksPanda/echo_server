from socket import *
from time import sleep
from threading import Thread, enumerate


class Server:
    def __init__(self) -> None:
        self.HOST = "127.0.0.1"
        self.PORT = 54321
        self.threads = enumerate()
        self.connections = {}

    def connect(self, s):
        while True:
            s.listen(1)
            conn, addr = s.accept()
            self.connections.update({addr: conn})
            self.threads.append(
                Thread(target=self.connect, args=(s,), daemon=False))
            self.threads[-1].start()
            print(self.threads)
            with conn:
                print("connected by", addr)
                while True:
                    try:
                        data = conn.recv(1024)
                        print(f"received from {addr}: {data.decode()}")
                        if not data:
                            break
                        data = self.check_command(data.decode(), conn, addr)
                    except:
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
        elif command.isnumeric():
            self.repeat(string[1:], command, conn)
        else:
            self.send_message(string, conn)

    def connection_loop(self):
        with socket() as s:
            s.bind((self.HOST, self.PORT))
            while True:
                self.connect(s)

    def broadcast(self, string, addr):
        for conn in self.connections.values():
            self.send_message(f"from {addr}: {string}", conn)


def main():
    Server().connection_loop()


if __name__ == "__main__":
    main()
