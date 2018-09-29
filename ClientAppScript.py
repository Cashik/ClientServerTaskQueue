"""
To test this run MyServer first.

example of commands:

python ClientAppScript.py -h
python ClientAppScript.py -c add_task -t shake_string -s 0123445
python ClientAppScript.py -c add_task -t reverse_string -s 0123445
python ClientAppScript.py -c task_status -i 3
python ClientAppScript.py -c task_result -i 10
python ClientAppScript.py -b -c add_task -t shake_string -s 0123445
"""

import argparse
import time
from MyClient import MyClient

server_tasks = ("reverse_string", "shake_string")
client_commands = ("add_task", "task_status", "task_result")

parser = argparse.ArgumentParser(
    description='''My Description. And what a lovely description it is. ''',
    epilog="""All's well that ends well.""")
parser.add_argument('-b', '--batch', help='Turn batch mode. Default is simple mode.', action="store_true")
parser.add_argument('-c', '--command', type=str, choices=client_commands,
                    help='Command to run on server: add_task, task_status or task_result.')
parser.add_argument('-t', '--task_name', type=str, choices=server_tasks,
                    help='Task name to execute it on server. Used with -c add_task.')
parser.add_argument('-s', '--string', type=str,
                    help='String that needs to be processed on server. Used with -c add_task.')
parser.add_argument('-i', '--task_id', type=str, help='Used with -c task_status or -c task_result.')
args = parser.parse_args()

client = MyClient()
if args.batch:
    if args.command == "add_task" or args.command is None:
        if args.task_name and args.string:
            result_data = client.call_task(args.task_name, [args.string])
            id = result_data.get('data', -1)
            if id != -1:
                print("Successfully adding a task to the queue. Task id:{}.".format(id))
                try:
                    status = 'WORK'
                    while status != 'COMPLETED' and status != 'ERROR':
                        task_status_response = client.get_task_status(id)
                        try:
                            status = task_status_response['data']
                        except KeyError:
                            status = task_status_response['error']

                        print("Task status is {}.".format(status))
                        time.sleep(1)
                except KeyboardInterrupt as e:
                    print("Process stopped by user.")

                task_result_response = client.get_task_result(id)
                try:
                    result = task_result_response['data']
                except KeyError:
                    result = task_result_response['error']
                print("Result is: {}".format(result))
            else:
                print("Error adding task. Server response: {}.".format(result_data.get('error', 'unknown error')))
        else:
            print("FatalError: <task_name> and <string> option is required for batch mode.")
    else:
        print("FatalError: only add_task value  available <command> option for this mode and is used by default.")

else:
    result_msg = ""
    error_msg = ""
    if args.command == "add_task":
        if args.task_name and args.string:
            response = client.call_task(args.task_name, [args.string])
            try:
                result_msg = response['data']
            except KeyError:
                result_msg = response['error']
        else:
            error_msg = "FatalError: <task_id> and <string> option required with add_task command."
    elif args.command == "task_status":
        if args.task_id:
            response = client.get_task_status(args.task_id)
            try:
                result_msg = response['data']
            except KeyError:
                result_msg = response['error']
        else:
            error_msg = "FatalError: <task_id> option required with task_status command."
    elif args.command == "task_result":
        if args.task_id:
            response = client.get_task_result(args.task_id)
            try:
                result_msg = response['data']
            except KeyError:
                result_msg = response['error']
        else:
            error_msg = "FatalError: <task_id> option required with task_result command."
    else:
        error_msg = "FatalError: <command> option is required."

    if error_msg:
        print(error_msg)
    else:
        print(result_msg)
