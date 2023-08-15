# task/executable.py
from abc import ABC, abstractmethod
import subprocess
import os
import datetime


from abc import ABC, abstractmethod
import os
import re


class BaseExecutable(ABC):
    def execute(self):
        self._pre_execution_hook()
        self._execute_task()
        self._post_execution_hook()

    def _pre_execution_hook(self):
        print("Pre-execution setup and checks")

    @abstractmethod
    def _execute_task(self):
        pass

    def _post_execution_hook(self):
        print("Post-execution cleanup and actions")

    def benchmark(self):
        """
        Execute the benchmark process.
        """
        self.load_model()
        self.prepare_data()
        self.run_inference()
        self.collect_results()

    def prepare_data(self):
        """
        Prepare the data for the benchmarking process.
        """
        pass

    def collect_results(self):
        """
        Collect and analyze performance results.
        """
        print("Collecting and analyzing performance results...")


class Executable(BaseExecutable):
    # 定义模板
    model_train_template = r"""
#!/bin/bash
set -e
set -x

# 获取当前脚本所在目录的绝对路径
script_dir=$(realpath "$(dirname "$0")")
# 设置工作目录
workspace="$script_dir/workspace"
mkdir -p $workspace || true

if [ "$XBENCHFLOW_INTERNAL_PROXY" = "true" ]; then
    # 设置代理配置
    git config --global http.proxy "http://agent.xxxxx.com:xxxx"
    git config --global https.proxy "https://agent.xxxxx.com:xxxx"
fi

# 检查是否已经 clone 了仓库
if [ -d "$workspace/{repo_name}" ]; then
    echo "Repository already cloned."
else
    # 克隆仓库
    git clone {github_url} "$workspace/{repo_name}"
    # 切换到指定 commit
    cd "$workspace/{repo_name}"
    git checkout {commit_hash}
    # 尝试安装, 如果存在setup.py
    if [ -f "setup.py" ]; then
        timeout 1200 python setup.py install || true
    fi
fi

# 切换到需要执行的目录并执行命令
cd "$workspace/{execution_path}"

# 获取当前 Git 代理配置
if [ "$XBENCHFLOW_INTERNAL_PROXY" = "true" ]; then
    git config --global --get http.proxy
    git config --global --get https.proxy
fi

# 执行主要命令
{execution_command}
"""

    def __init__(self, data_list, args):
        super().__init__()
        self.model_list = data_list
        self.args = args

    def _execute_task(self):
        # 实现具体的任务逻辑
        pass

    def execute(self):
        executable_mapping = self._process_and_generate_scripts(
            self.model_list, self.args
        )
        return executable_mapping

    @staticmethod
    def _generate_script_content(config_dict):
        github_url = config_dict["github_url"]
        repo_name = Executable._get_repo_name(github_url)

        commit_hash = config_dict["commit"]
        execution_path = config_dict["execution_path"]
        execution_command = Executable._replace_batch_size_undecided(
            config_dict["execution_command"], config_dict["default_batch_size"]
        )

        script_content = Executable.model_train_template.format(
            commit_hash=commit_hash,
            repo_name=repo_name,
            github_url=github_url,
            execution_path=execution_path,
            execution_command=execution_command,
        )
        return script_content

    @staticmethod
    def _get_repo_name(github_url):
        last_slash_index = github_url.rfind("/")
        git_extension_index = github_url.find(".git")
        return github_url[last_slash_index + 1 : git_extension_index]

    @staticmethod
    def _replace_batch_size_undecided(execution_command, default_batch_size):
        pattern = r"\bbatch_size_undecided\b"
        return re.sub(pattern, str(default_batch_size), execution_command)

    @staticmethod
    def _process_and_generate_scripts(data_list, args):
        model_script_mapping = (
            {}
        )  # Used to collect model names and corresponding script paths

        filt_word = args.keyword

        for config_dict in data_list:
            if filt_word and filt_word not in config_dict['model_name']:
                continue
            script_content = Executable._generate_script_content(config_dict)
            script_filename = f"run_{config_dict['num_devices']}_{config_dict['model_name']}_script.sh"
            script_abs_path = os.path.abspath(script_filename)
            bash_executable = f"bash {script_abs_path}"
            model_script_mapping[
                config_dict["model_name"]
            ] = bash_executable  # Update the dictionary

            with open(script_filename, "w") as script_file:
                script_file.write(script_content)

            print(f"Generated script: {script_abs_path}")

        return model_script_mapping  # Return the dictionary


class TaskExecutable(Executable):
    def execute(self, task_id, sleep_time):
        pid = os.getpid()
        ppid = os.getppid()

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        print(f"[{current_time}][p {pid}][t {task_id}] Task {task_id} started")

        cmd = f"sleep {sleep_time} && echo 'Task {task_id} finished after sleeping {sleep_time} seconds'"
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

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
