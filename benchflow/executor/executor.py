# executor/executor.py
class Executor:
    def run(self, executable, **kwargs):
        """
        执行模型训练或推理任务。

        Args:
            executable (Executable): 要执行的任务对象.
            **kwargs: 可变参数，用于传递执行任务所需的其他参数.
        """
        executable.execute(**kwargs)
