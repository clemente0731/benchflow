import os
import sys
import subprocess
import concurrent.futures
import argparse
from termcolor import colored


def find_python_files(root_dir):
    python_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    print(python_files)
    return python_files


def format_file(file):
    try:
        before_format = open(file).read()
        subprocess.run(["python", "-m", "black", file], check=True)
        after_format = open(file).read()
        print(colored(f"Formatted: {file}", "green"))
        print(colored("Before format:", "red"))
        print(before_format)
        print(colored("After format:", "green"))
        print(after_format)
    except subprocess.CalledProcessError as e:
        print(f"Error formatting {file}: {e}")


def check_format_file(file):
    try:
        before_format = open(file).read()
        subprocess.run(["python", "-m", "black", "--check", file], check=True)
        after_format = open(file).read()
        print(colored(f"Format is correct: {file}", "green"))
        print(colored("Before format:", "red"))
        print(before_format)
        print(colored("After format:", "green"))
        print(after_format)
    except subprocess.CalledProcessError as e:
        print(f"Format is incorrect for {file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch execute black format on Python files."
    )
    parser.add_argument(
        "mode",
        choices=["format", "check_format"],
        default="format",
        help="Choose the mode: format or check_format",
    )
    args = parser.parse_args()

    # 搜索全局git内的Python文件
    root_dir = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip()
    python_files = find_python_files(root_dir)

    # 并发执行20个进程
    with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor:
        if args.mode == "format":
            # 格式化文件
            futures = [executor.submit(format_file, file) for file in python_files]
        elif args.mode == "check_format":
            # 检查格式
            futures = [
                executor.submit(check_format_file, file) for file in python_files
            ]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
