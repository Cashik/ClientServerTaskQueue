import threading
from queue import Queue

from Task import Task


class TasksQueue:

    def __init__(self):
        # contain ids
        self.tasks_queue = Queue()
        # new_task_id:int -> Task
        self.tasks = {}

        self.is_running = False
        self.is_enable = False

    def run(self):
        self.is_enable = True

        thread = threading.Thread(target=self._start_worker)
        thread.setDaemon(True)
        thread.start()

    def stop(self):
        self.is_enable = False

    def _start_worker(self):
        self.is_running = True
        while not self.tasks_queue.empty() and self.is_enable:
            task_id_to_run = self.tasks_queue.get()
            # don't need to catch KeyError until the remove task method is implemented
            self.tasks[task_id_to_run].run()
        self.is_running = False

    def add_task(self, new_task: Task) -> int:
        # trying to catch an error in the logic of the gen of new_task_id
        if self.tasks.get(new_task.id, False):
            raise KeyError("Task new_task_id {} is already taken.".format(new_task.id))

        self.tasks_queue.put(new_task.id)
        self.tasks[new_task.id] = new_task

        # restart worker if it stopped
        if not self.is_running and self.is_enable:
            self.run()

        return new_task.id

    # TODO: this method really need?
    def get_task_by_id(self, task_id: str):
        if type(task_id)!=str:
            return None
        return self.tasks.get(task_id, None)


if __name__ == "__main__":

    import random
    import time


    def print_tasks_queue(q: TasksQueue):
        cmd_row = ""
        for task in q.tasks.items():
            cmd_row += str(task) + "\t|\t"
        print(cmd_row)


    def fnc():
        result = random.randint(1, 5)
        time.sleep(result)
        return result


    q = TasksQueue()

    for i in range(3):
        q.add_task(Task(str(i + 1), fnc))

    q.run()

    while q.is_running:
        print_tasks_queue(q)
        time.sleep(0.5)

    q.add_task(Task("additional task", fnc))

    while q.is_running:
        print_tasks_queue(q)
        time.sleep(0.5)

    print("Final:")
    print_tasks_queue(q)
