# task/executable.py
from abc import ABC, abstractmethod
import subprocess
import os
import datetime

class Executable(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        """
        执行任务的抽象方法。

        Args:
            **kwargs: 可变参数，用于传递执行任务所需的其他参数。
        """
        pass


class TaskExecutable(Executable):
    def execute(self, task_id, sleep_time):
        pid = os.getpid()
        ppid = os.getppid()

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        print(f"[{current_time}][p {pid}][t {task_id}] Task {task_id} started")

        cmd = f"sleep {sleep_time} && echo 'Task {task_id} finished after sleeping {sleep_time} seconds'"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        while True:
            output = process.stdout.readline().strip()
            if not output and process.poll() is not None:
                break
            if output:
                print(f"[{current_time}][p {pid}][pp {ppid}][t {task_id}] {output}")

        return process.returncode

class BenchmarkTask(Executable):
    def execute(self, **kwargs):
        # 在这里实现基准测试的具体逻辑
        print("Running benchmark...")
        # 可以调用其他模块中的功能函数，或执行外部命令等
        pass


class POCValidationTask(Executable):
    def execute(self, **kwargs):
        # 在这里实现验证 POC 的具体逻辑
        print("Running POC validation...")
        # 可以调用其他模块中的功能函数，或执行外部命令等
        pass


class AutomationTask(Executable):
    def execute(self, **kwargs):
        # 在这里实现自动化任务的具体逻辑
        print("Running automation...")
        # 可以调用其他模块中的功能函数，或执行外部命令等
        pass
