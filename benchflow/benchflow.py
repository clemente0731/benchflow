#!/usr/bin/env python

import pandas as pd
import re

# from benchflow.task.benchmark import HuggingfaceTransformers, FlagOpenFlagPerf
from benchflow.modelzoo.model_meta import ModelInfoParser
from benchflow.utils.ascii_builder import generate_benchflow_logo, generate_model_list_logo, torch_collect_env_info


def run_benchflow():
    import argparse

    benchflow_logo = generate_benchflow_logo()
    print(benchflow_logo)

    parser = argparse.ArgumentParser(
        description="Benchmark machine learning models using the OpenModelZooBenchmark template class."
    )
    # parser.add_argument(
    #     "model",
    #     choices=["huggingface", "flagopenflagperf"],
    #     nargs="?",
    #     help="The machine learning model to benchmark (choose from 'huggingface' or 'flagopenflagperf').",
    # )

    # if args.model == "huggingface":
    #     print("Benchmarking Model A from Huggingface Transformers...")
    #     model_a = HuggingfaceTransformers()
    #     model_a.benchmark()
    # elif args.model == "flagopenflagperf":
    #     print("Benchmarking Model B from FlagOpenFlagPerf...")
    #     model_b = FlagOpenFlagPerf()
    #     model_b.benchmark()

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

    parser = ModelInfoParser()
    model_info_list = parser.parse_csv_file()

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
            parser = ModelInfoParser()
            model_info_list = parser.parse_csv_file()
            for model_info in model_info_list:
                model_name = model_info.info.model_name
                if re.search(args.keyword, model_name, re.IGNORECASE):
                    filtered_models.append(model_info)
            model_info_list = filtered_models

        parser.print_model_info_list_with_pandas(model_info_list)


if __name__ == "__main__":
    run_benchflow()
