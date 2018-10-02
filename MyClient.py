import json
import socket
from MyServer import DEFAULT_SERVER_ADDRESS, receive_all_json, \
    DEFAULT_REQUEST_TIMEOUT


class MyClient:

    def __init__(self, server_address: tuple = None, response_timeout: float = DEFAULT_REQUEST_TIMEOUT):
        if server_address is None:
            server_address = DEFAULT_SERVER_ADDRESS
        self.server_address = server_address
        self.response_timeout = response_timeout

    def send_data(self, data: str) -> str:
        try:
            # Create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect the socket to the port where the server is listening
            sock.connect(self.server_address)
            try:
                # Send data
                sock.sendall(data.encode())
                # Look for json data
                sock.settimeout(self.response_timeout)
                response_data = receive_all_json(sock)
            finally:
                sock.close()
        except (ConnectionAbortedError, ConnectionResetError, ConnectionRefusedError):
            response_data = '{"error": "No response from the server."}'

        return response_data

    def call_task(self, task_name: str, args: list = [], kwargs: dict = {}) -> dict:
        # send request and data
        request_json = {'meta': {'method_name': 'add_task'},
                        'data': {'task_name': task_name, 'args': args, 'kwargs': kwargs}}
        return json.loads(self.send_data(json.dumps(request_json)))

    def get_task_status(self, task_id: int) -> dict:
        # send request and data
        request_json = {'meta': {'method_name': 'task_status'},
                        'data': {'id': task_id}}
        return json.loads(self.send_data(json.dumps(request_json)))

    def get_task_result(self, task_id: int) -> dict:
        # send request and data
        request_json = {'meta': {'method_name': 'task_result'},
                        'data': {'id': task_id}}
        return json.loads(self.send_data(json.dumps(request_json)))


if __name__ == "__main__":
    import time

    client = MyClient()

    print("Add reverse string task:", client.call_task("reverse_string", args=["parametr to print"]))
    print("Add shake_string task:", client.call_task("shake_string", args=["012345"]))
    print("Add reverse string task with very long string:",
          client.call_task("reverse_string", args=["parametr to print" * 1000]))

    while True:
        print("shake_string func status and result with long string:", client.get_task_status('2'),
              client.get_task_result('2'))
        time.sleep(0.5)
