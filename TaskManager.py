import json
from json import JSONDecodeError

import TasksCollector
from Task import Task
from TasksQueue import TasksQueue


class TaskManager(TasksQueue):

    def handle_command(self, command_json: str) -> dict:
        try:
            command = json.loads(command_json)

            if command.get('error', False):
                # command already contain error msg
                response_data = command
            elif command.get('meta', {}).get('method_name', '') == "add_task":
                try:
                    # get func obj
                    func = getattr(TasksCollector, command['data']['task_name'])
                    # setup task
                    new_task = Task(command['data']['task_name'], func)
                    new_task.set_params(*command['data']['args'], **command['data']['kwargs'])
                    # get task new_task_id tu return
                    result = self.add_task(new_task)
                    response_data = {"data": result}
                except (AttributeError, TypeError):
                    response_data = {"error": "No such task name"}
            elif command.get('meta', {}).get('method_name', '') == "task_status":
                task = self.get_task_by_id(command['data']['id'])
                if task:
                    response_data = {"data": task.state.name}
                else:
                    response_data = {"error": "No such task id"}
            elif command.get('meta', {}).get('method_name', '') == "task_result":
                task = self.get_task_by_id(command['data']['id'])
                if task:
                    response_data = {"data": task.result}
                else:
                    response_data = {"error": "No such task id"}
            else:
                raise KeyError()
        except (KeyError, JSONDecodeError):
            response_data = {"error": "Invalid request", "request": str(command)}

        return response_data


if __name__ == "__main__":
    t_m = TaskManager()

    commands = [{'error': 'some mesage'},

                {"meta": {'method_name': 'add_task'},
                 'data': {"task_name": 'some wrong task', 'new_task_id': 5}},

                {'meta': {'method_name': 'add_task'},
                 'data': {'task_name': 'shake_string', 'args': ['right parameter'],
                          'kwargs': {'wrong_param': 'argument string'}}},

                {'meta': {'method_name': 'add_task'},
                 'data': {'task_name': 'shake_string', 'args': ['right parameter'],
                          'kwargs': {}}},

                {'meta': {'method_name': 'shake_string'},
                 'data': {'kwargs': {'wrong_param': 'argument string'}}},

                {'meta': {'method_name': 'get_task_status'}, 'data': {'id': 0}},
                {'meta': {'method_name': 'get_task_status'}, 'data': {'id': '0'}},
                {'meta': {'method_name': 'get_task_status'}, 'data': {'id': '2'}},
                {'meta': {'method_name': 'get_task_status'}, 'data': {'id': {}}},
                {'meta': {'method_name': 'get_task_result'}, 'data': {'id': 0}},
                {'meta': {'method_name': 'get_task_result'}, 'data': {'id': '0'}},
                ]

    for command in commands:
        command_text = json.dumps(command)
        print("Command and request:")
        print(command_text)
        print(t_m.handle_command(command_text))
        print()
