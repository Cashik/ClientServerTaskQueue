import json
import socket


class MyClient:

    def __init__(self, server_address: tuple = None):
        if server_address is None:
            server_address = ('localhost', 10000)
        self.server_address = server_address

    def send_data(self, data: str) -> str:
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        self.sock.connect(self.server_address)
        # Send data
        self.sock.sendall(data.encode())
        # Look for the response
        data = self.sock.recv(1024).decode()
        self.sock.close()

        return data

    def call_task(self, task_name: str, args: list = [], kwargs: dict = {}) -> dict:
        # send request and data
        request_json = {'meta': {'method_name': 'add_task'},
                        'data': {'task_name': task_name, 'args': args, 'kwargs': kwargs}}
        return json.loads(self.send_data(json.dumps(request_json)))

    def get_task_status(self, task_id: int) -> dict:
        # send request and data
        request_json = {'meta': {'method_name': 'get_task_status'},
                        'data': {'id': task_id}}
        return json.loads(self.send_data(json.dumps(request_json)))

    def get_task_result(self, task_id: int) -> dict:
        # send request and data
        request_json = {'meta': {'method_name': 'get_task_result'},
                        'data': {'id': task_id}}
        return json.loads(self.send_data(json.dumps(request_json)))


if __name__ == "__main__":
    import threading
    import time

    client = MyClient()

    print("Add reverse string task:", client.call_task("reverse_string", args=["parametr to print"]))
    print("Add shake_string task:", client.call_task("shake_string", args=["012345"]))

    while True:
        print("shake_string func status and result:", client.get_task_status(1), client.get_task_result(1))
        time.sleep(0.5)
