#!/usr/bin/env python

import pandas as pd
import re
import os
# from benchflow.task.benchmark import HuggingfaceTransformers, FlagOpenFlagPerf
from benchflow.modelzoo.model_meta import ModelInfoLoader
from benchflow.task.executable import Executable
from benchflow.executor.executor import Executor
from benchflow.utils.ascii_builder import (
    generate_benchflow_logo,
    generate_model_list_logo,
    torch_collect_env_info,
)


def run_benchflow():
    import argparse
    print("\nBenchflow ==> Initializing... Please wait...   ")
    benchflow_logo = generate_benchflow_logo()
    print(benchflow_logo)

    parser = argparse.ArgumentParser(
        description="Benchmark machine learning models using the OpenModelZooBenchmark template class."
    )

    # 设置 usage 信息
    usage_examples = """
    Examples:
    benchflow -l -k resnet
    benchflow -l
    benchflow -t poc -d xla
    benchflow -t poc -d xla -k resnet
    benchflow -t benchmark -d gpu
    benchflow -t benchmark -d gpu -k resnet
    benchflow -t automatic_search -d xla
    benchflow -t automatic_search -d xla -k resnet
    """

    parser.usage = f"benchflow [options]\n{usage_examples}"

    parser.add_argument(
        "-d",
        "--device",
        choices=["xla", "gpu"],
        default="gpu",  # 设置默认设备类型为 "gpu"
        required=False,  # 将设备选项设置为必须
        help="The device type to use (choose from 'xla' or 'gpu'). Default: XLA_VISIBLE_DEVICES=0 or CUDA_VISIBLE_DEVICES=0 .",
    )

    parser.add_argument(
        "-w",
        "--workspace",
        nargs="?",
        default=os.getcwd(),  # 设置默认值为当前命令行执行的目录
        help="The workspace directory for task execution.",
    )
    parser.add_argument(
        "-t",
        "--task",
        choices=["poc", "benchmark", "automatic_search"],
        nargs="?",
        help="The machine learning task to benchmark (choose from 'poc', 'benchmark', or 'automatic_search').",
    )
    parser.add_argument(
        "-l",
        "--list",
        dest="list",
        action="store_true",
        help="If provided, benchmark multiple machine learning models.",
    )
    parser.add_argument(
        "-k",
        "--keyword",
        dest="keyword",
        metavar="KEYWORD",
        nargs="?",
        const="",
        help="Filter models by name using regex pattern KEYWORD.",
    )


    args = parser.parse_args()

    parser = ModelInfoLoader()
    model_info_list = parser.load_model_info()

    if args.task == "poc":
        print("Benchmarking poc task...")
        # Your poc benchmarking code here
    elif args.task == "benchmark":
        print("Benchmarking benchmark task...")
        # Your benchmarking code here
    elif args.task == "automatic_search":
        print("Benchmarking automatic_search task...")
        # Your automatic_search benchmarking code here

    if args.list:
        model_list_logo = generate_model_list_logo()
        print(model_list_logo)

        if args.keyword:
            filtered_models = []
            parser = ModelInfoLoader()
            model_info_list = parser.load_model_info()
            for model_info in model_info_list:
                model_name = model_info["model_name"]
                if re.search(args.keyword, model_name, re.IGNORECASE):
                    filtered_models.append(model_info)
            model_info_list = filtered_models

        parser.print_model_info_list(model_info_list)
    else:
        if args.keyword:
            loader = ModelInfoLoader()
            loader.print_model_info_list()
            model_info = loader.load_model_info()
            executable = Executable(model_info, args)
            executor = Executor(executable)
            executor.run()


if __name__ == "__main__":
    run_benchflow()
