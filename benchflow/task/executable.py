# task/executable.py
from abc import ABC, abstractmethod

class Executable(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        """
        执行任务的抽象方法。

        Args:
            **kwargs: 可变参数，用于传递执行任务所需的其他参数。
        """
        pass


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
