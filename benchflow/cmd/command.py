import subprocess
import multiprocessing


class Command:
    def __init__(self):
        pass

    def run_command(self, command):
        """
        执行外部命令并返回执行结果。

        Args:
            command (str): 要执行的外部命令.

        Returns:
            subprocess.CompletedProcess: 命令的执行结果，包含返回码和输出内容等信息。
        """
        try:
            # 使用 subprocess.run 执行 Bash 脚本，并捕获标准输出和错误输出
            result = subprocess.run(
                command,
                executable="/bin/bash",
                shell=True,
                capture_output=True,
                text=True,
            )

            # subprocess.run 执行命令后的返回值为 subprocess.CompletedProcess 对象，
            # 包含以下属性：
            # - args: 执行的命令行参数，是一个字符串或一个序列。
            # - returncode: 命令的返回码，如果命令成功执行，则返回0，否则返回其他非零值。
            # - stdout: 命令的标准输出内容，以字符串形式存储。
            # - stderr: 命令的标准错误输出内容，以字符串形式存储。

            # 如果命令执行成功，返回执行结果
            if result.returncode == 0:
                return result
            else:
                # 如果命令执行失败，输出错误信息并返回None
                print(
                    f"Command '{command}' failed with return code {result.returncode}"
                )
                print(result.stderr)
                return None

        except Exception as e:
            # 捕获异常，输出错误信息并返回None
            print(f"Error occurred while executing command '{command}': {str(e)}")
            return None

    def run_commands_in_parallel(self, commands):
        """
        并行执行多个外部命令，并返回执行结果列表。

        Args:
            commands (list): 包含多个要执行的外部命令的列表.

        Returns:
            list: 包含所有命令的执行结果的列表。
        """
        # 使用多进程池，设置进程数量为 CPU 核心数
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

        # 使用多进程池的 map 方法并行执行多个命令
        results = pool.map(self.run_command, commands)

        # 关闭进程池
        pool.close()
        pool.join()

        return results


# if __name__ == "__main__":
#     commands = ["ls -alt", "echo 'Hello World'", "ls -a"]
#     cmd = Command()
#     results = cmd.run_commands_in_parallel(commands)
#     for result in results:
#         if result is not None:
#             print(result.stdout)
