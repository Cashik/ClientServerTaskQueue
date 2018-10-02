import json
import socket

from TaskManager import TaskManager

DEFAULT_SERVER_ADDRESS = ("localhost", 10000)
SERVER_PACKET_SIZE = 1024
SERVER_SOCKET_TIMEOUT = 0.5
SERVER_RECEIVE_TIMEOUT_MILLISECONDS = 1000
SERVER_LISTEN_CONNECTIONS = 1
DEFAULT_REQUEST_TIMEOUT = 0.5
DEFAULT_RESPONSE_TIMEOUT = 0.5


def is_json(mb_json):
    try:
        json.loads(mb_json)
    except ValueError:
        return False
    return True


def receive_all_json(sock) -> str:
    received_json = str()
    while not is_json(received_json):
        try:
            data = sock.recv(SERVER_PACKET_SIZE)
            received_json += data.decode()
            if is_json(received_json):
                return received_json
        except socket.timeout:
            return json.dumps({'error': 'timeout error'})


class MyServer:

    def __init__(self, server_address: "tuple (ip,port)" = None):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if server_address is None:
            server_address = DEFAULT_SERVER_ADDRESS
        self.sock.bind(server_address)
        self.sock.listen(SERVER_LISTEN_CONNECTIONS)
        self.sock.settimeout(SERVER_SOCKET_TIMEOUT)
        self.response_timeout = DEFAULT_RESPONSE_TIMEOUT

        self.running = False
        self.task_manager = TaskManager()
        self.task_manager.run()

    def run(self):
        self.running = True
        try:
            while self.running:
                print('Waiting for a new connection on ', self.sock)
                # Wait for a connection
                connection = None
                while not connection and self.running:
                    try:
                        connection, client_address = self.sock.accept()
                    except socket.timeout:
                        pass
                self.handle_connection(connection)

        except KeyboardInterrupt:
            print('Server closing by user.')
        finally:
            self.running = False
            self.sock.close()

    def stop(self):
        self.running = False

    def handle_connection(self, connection):
        try:
            connection.settimeout(self.response_timeout)
            json_request = receive_all_json(connection)
            # print("Request:", json_request)
            answer = self.task_manager.handle_command(json_request)
            # print('Answer:', answer)
            connection.sendall(json.dumps(answer).encode())
        except (ConnectionAbortedError, ConnectionResetError, ConnectionRefusedError):
            pass
        finally:
            connection.close()


if __name__ == "__main__":
    # run this script to make server alive
    server = MyServer()
    server.run()
