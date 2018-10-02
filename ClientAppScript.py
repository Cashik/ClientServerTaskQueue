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
import json
import sys
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
            new_task_id = result_data.get('data', -1)
            if new_task_id != -1:
                print("Successfully adding a task to the queue. New task id: {}.".format(new_task_id))
                try:
                    status = '???'
                    while status != 'COMPLETED' and status != 'ERROR':
                        task_status_response = client.get_task_status(new_task_id)
                        try:
                            status = task_status_response['data']
                            print("Task status is {}.".format(status))
                        except KeyError:
                            status = task_status_response['error']
                            print("Error: {}.".format(status))

                        time.sleep(1)
                except KeyboardInterrupt as e:
                    print("Process stopped by user.")

                task_result_response = client.get_task_result(new_task_id)
                try:
                    result = task_result_response['data']
                    print("Result is: {}".format(result))
                except KeyError:
                    result = task_result_response['error']
                    print("Result is unknown. Error: {}.".format(result))

            else:
                print("Error adding task: '{}'.".format(result_data.get('error', 'unknown error')))
        else:
            print("FatalError: <task_name> and <string> option is required for batch mode.")
    else:
        print("FatalError: only add_task value  available <command> option for this mode and is used by default.")

else:
    result_msg = ""
    error_msg = ""

    # check params structure
    if args.command == "add_task":
        if not (args.task_name and args.string):
            error_msg = "FatalError: <task_id> and <string> option required with add_task command."
    elif args.command == "task_status" or args.command == "task_result":
        if not args.task_id:
            error_msg = "FatalError: <task_id> option required with task_status and task_result command."
    else:
        error_msg = "FatalError: <command> option is required."

    # terminate if error
    if error_msg:
        print(error_msg)
        sys.exit(2)

    # prepare raw request
    request = {'meta': {'method_name': args.command},
               'data': {
                   'task_name': args.task_name,
                   'id': args.task_id,
                   'string': args.string,
                   'kwargs': {},
                   'args': [args.string] if args.string else [],
               }
               }

    request_json = json.dumps(request)
    # get client response
    response_json = client.send_data(request_json)

    response = json.loads(response_json)
    if response.get('data', False):
        print("Server response with data: {}".format(response['data']))
    else:
        print("Server response with error: {}".format(response['error']))


