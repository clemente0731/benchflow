import random
from benchflow.task.executable import (
    Executable,
    TaskExecutable,
    BenchmarkTask,
    POCValidationTask,
    AutomationTask,
)
import multiprocessing


class Executor:
    def __init__(self, num_processes):
        self.num_processes = num_processes
        self.process_list = []
        self.result_queue = multiprocessing.Queue()

    def process_worker(self, task_id, executable, **kwargs):
        result = executable.execute(task_id, **kwargs)
        self.result_queue.put(result)
        print(f"Task {task_id} completed")

    def run(self, executable, **kwargs):
        print("Starting processes...")
        for task_id in range(self.num_processes):
            process = multiprocessing.Process(
                target=self.process_worker, args=(task_id, executable, kwargs)
            )
            self.process_list.append(process)
            process.start()

        for process in self.process_list:
            process.join()

        print("All processes completed. Results:")
        while not self.result_queue.empty():
            result = self.result_queue.get()
            print(f"Process return code: {result}")


# class TaskExecutor(Executor):
#     def execute(self, executable, task_id, sleep_time):
#         executable.execute(task_id, sleep_time)

# def main():
#     num_processes = 2
#     executor = TaskExecutor()

#     print("Starting processes...")
#     for task_id in range(num_processes):
#         sleep_time = random.randint(1, 10)
#         executable = TaskExecutable()
#         executor.run(executable, task_id=task_id, sleep_time=sleep_time)

#     print("All processes completed.")
