import threading
from queue import Queue

from Task import Task


class TasksQueue:

    def __init__(self):
        self.tasks = []
        self.current_task = 0
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            if self.current_task == len(self.tasks):
                # nothing to do
                pass
            elif self.current_task < len(self.tasks):
                self.tasks[self.current_task].run()
                self.current_task += 1
            else:
                raise ValueError("How?")

    def add_task(self, task: Task) -> int:
        self.tasks.append(task)
        return len(self.tasks) - 1

    def get_task_by_id(self, task_id):
        return self.tasks[task_id]


if __name__ == "__main__":

    import random
    import time


    def fnc():
        result = random.randint(1, 10)
        time.sleep(result)
        return result


    q = TasksQueue()

    for i in range(5):
        q.add_task(Task(str(i), fnc))

    while True:
        cmd_row = ""
        for task in q.tasks:
            cmd_row += str(task) + "\t|\t"
        print(cmd_row)
        time.sleep(0.5)
