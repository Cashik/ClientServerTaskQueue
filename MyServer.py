import json
import socket

import TasksCollector
from Task import Task
from TasksQueue import TasksQueue


class MyServer:

    def __init__(self, server_address: "tuple (ip,port)" = None):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if server_address == None:
            server_address = ("localhost", 10000)
        self.sock.bind(server_address)

        self.running = False
        self.worker = TasksQueue()

    def run(self):
        self.running = True
        self.sock.listen(1)

        # TODO: its unstoppable)
        while self.running:
            # Wait for a connection
            print('waiting for a new connection on ', self.sock)
            connection, client_address = self.sock.accept()
            # thread.start_new_thread(self.handle_connection, (connection, client_address))
            self.handle_connection(connection, client_address)

    def stop(self):
        self.running = False

    def handle_connection(self, connection, address):

        while True:
            try:
                request_text = connection.recv(1024).decode()

                if request_text:
                    request_data = json.loads(request_text)
                    if request_data['meta']['method_name'] == "add_task":
                        try:
                            # get func obj
                            func = getattr(TasksCollector, request_data['data']['task_name'])

                            new_task = Task(request_data['data']['task_name'], func)
                            new_task.set_params(*request_data['data']['args'], **request_data['data']['kwargs'])

                            result = self.worker.add_task(new_task)
                            response_data = {"data": result}
                        except (AttributeError, TypeError):
                            response_data = {"error": "No such task name"}

                    elif request_data['meta']['method_name'] == "get_task_status":
                        try:
                            response_data = {
                                "data": self.worker.get_task_by_id(int(request_data['data']['id'])).state.name}
                        except IndexError:
                            response_data = {"error": "No such task id"}
                        except (KeyError, TypeError) as e:
                            response_data = {"error": str(e)}

                    elif request_data['meta']['method_name'] == "get_task_result":
                        try:
                            response_data = {"data": self.worker.get_task_by_id(int(request_data['data']['id'])).result}
                        except IndexError:
                            response_data = {"error": "No such task id"}
                        except (KeyError, TypeError) as e:
                            response_data = {"error": str(e)}
                    else:
                        response_data = "unknown request"

                    connection.sendall(json.dumps(response_data).encode())
                else:
                    break
            except (ConnectionAbortedError, ConnectionResetError):
                break

        connection.close()


if __name__ == "__main__":
    # run this script to make server alive
    server = MyServer()
    server.run()
