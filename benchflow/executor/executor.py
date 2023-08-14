import random
from benchflow.task.executable import (
    Executable,
)
import multiprocessing
import subprocess
import os
import random
import time
import inspect
import os
from pprint import pprint
import time
import functools


class ExecutorLegacy:
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


def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"Start time: {start_time}")
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"End time: {end_time}")

        duration = end_time - start_time

        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)

        print(
            f"Function '{func.__name__}' in file '{caller_info.filename}' at line {caller_info.lineno}:"
        )
        print(
            f"Start time: {start_time}, End time: {end_time}, Duration: {duration:.6f} seconds"
        )

        return result

    return wrapper


class ExecutableHandle:
    def validate_check(self, exec_input):
        # 在这里编写解析用户输入命令的逻辑
        # 验证命令的合法性，如果合法，返回解析后的命令，否则返回 None
        return exec_input.execute()


class TaskQueue:
    def __init__(self):
        self.queue = []

    def enqueue_task(self, task):
        self.queue.append(task)

    def dequeue_task(self):
        if self.queue:
            return self.queue.pop(0)
        return None


class ExecutionStatusManager:
    def __init__(self):
        self.status_map = {}
        self.last_print_time = time.time()
        self.print_interval = 60  # 控制打印的时间间隔，单位为秒

    def update_status(self, task_id, status):
        self.status_map[task_id] = status
        current_time = time.time()

        if current_time - self.last_print_time >= self.print_interval:
            print(f"Task {task_id} status updated: {status}")
            self.last_print_time = current_time

    def get_status(self, task_id):
        return self.status_map.get(task_id, "Unknown")


class Executor:
    def __init__(self, executable):
        self.executable = executable
        self.executable_args = self.executable.args
        self.task_handle = ExecutableHandle()
        self.task_queue = TaskQueue()
        self.status_manager = ExecutionStatusManager()

    @time_it
    def task_function(self, task_id, script_content, working_directory):
        pid = os.getpid()
        ppid = os.getppid()
        print(f"Task {task_id}: PID={pid}, PPID={ppid}, script: {script_content}")

        try:
            process = subprocess.Popen(
                args=script_content,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True,
                executable="/bin/bash",
                cwd=working_directory,
                bufsize=1,  # 设置缓冲为line
                universal_newlines=True,  # 为了确保输出是文本模式
                env=os.environ.copy(),  # 与当前环境变量保持一致
            )

            # 逐行读取标准输出和标准错误
            with process.stdout as stdout, process.stderr as stderr:
                for line in iter(stdout.readline, ""):
                    print(
                        f"Task {task_id} PID={pid}, PPID={ppid}, Standard Output: {line.strip()}",
                        flush=True,
                    )
                for line in iter(stderr.readline, ""):
                    print(
                        f"Task {task_id} PID={pid}, PPID={ppid}, Standard Error: {line.strip()}",
                        flush=True,
                    )

            returncode = process.wait()

            if returncode == 0:
                print(f"Task {task_id}: Command executed successfully.")
            else:
                print(
                    f"Task {task_id}: Command execution failed with return code {returncode}."
                )

            return returncode
        except Exception as e:
            print(f"Error occurred in Task {task_id}: {str(e)}")
            return None

    def run(self):
        self._execute_command()

    def _execute_command(self):
        commands = self.task_handle.validate_check(self.executable)
        if commands:
            for name, command in commands.items():
                task_id = len(self.task_queue.queue) + 1  # 为每个任务生成唯一 ID
                task = {"id": task_id, "model": name, "command": command}
                # time.sleep(100)
                self.task_queue.enqueue_task(task)
                self.status_manager.update_status(task_id, "Pending")

        return self._run_tasks()

    def _run_tasks(self):
        print("== Starting task execution")
        while True:
            task = self.task_queue.dequeue_task()
            if task:
                task_id = task["id"]
                model_name = task["model"]
                self.status_manager.update_status(task_id, "Running")
                print(f"\n\n-- Task {task_id} - {model_name} is now running.")
                status_update = self._execute_task(task)
                task_key = f"{task_id} -- {model_name}"
                self.status_manager.update_status(task_key, status_update)
                print(f"-- Task {task_id} - {model_name} has been completed.\n\n")
            else:
                print("== All tasks have been completed.")
                for idx, ret in self.status_manager.status_map.items():
                    if ret != "Running":
                        print(f"idx: {idx} -- ret: {ret}")
                break
        print("== All tasks have been completed.")

    def _execute_task(self, task):
        import time

        time.sleep(0.1)
        exec_ret = self.task_function(
            task["id"], task["command"], self.executable_args.workspace
        )
        print(f"Task {task['id']}-{task['model']} completed: {task['command']}")
        if exec_ret == 0:
            return "Pass"
        else:
            return "Failed"
