import threading
import time
from enum import Enum


class State(Enum):
    WAIT = 0
    WORK = 1
    COMPLETED = 2
    ERROR = 3


class Task:
    id_counter = 0

    def __init__(self, name: str, func: callable):
        self.id = str(Task.id_counter)
        Task.id_counter += 1

        self.name = name
        self.func = func
        self.state = State.WAIT
        self.func_args = []
        self.func_kwargs = {}
        self.result = None

    def set_params(self, *args, **kwargs):
        self.func_args = args
        self.func_kwargs = kwargs

    # set params for
    def run(self, ):
        self.state = State.WORK
        try:
            self.result = self.func(*self.func_args, **self.func_kwargs)
            self.state = State.COMPLETED
        except Exception as e:
            self.result = str(e)
            self.state = State.ERROR

    def __repr__(self):
        return "Task {}: {} {}".format(self.name, self.state.name, self.result)


if __name__ == "__main__":
    def some_work(data: str) -> str:
        time.sleep(3)
        return data[::-1]


    class SomeClass:

        def __init__(self):
            self.A = 5

        def inc(self):
            self.A += 1

        def add(self, B: int):
            self.A += B

        def smart_sub(self, B: int = 1) -> int:
            self.A -= B
            return self.A


    t1 = Task('some task', some_work)
    t1.set_params("String to reverse")
    print(t1)
    t1.run()
    print(t1)

    a = SomeClass()
    print("A=", a.A)
    t1 = Task('class method task inc', a.inc)
    print(t1)
    t1.run()
    print(t1)
    print("A=", a.A)

    t1 = Task('class method task smart_sub', a.smart_sub)
    t1.set_params(B=1)
    print(t1)
    t1.run()
    print(t1)
    print("A=", a.A)


    def CreateTask():
        t = Task("asdf", lambda: 2)
        print("Task new_task_id in another thread:{}".format(t.id))


    thread = threading.Thread(target=CreateTask)
    thread.start()
