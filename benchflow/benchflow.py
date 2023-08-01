#!/usr/bin/env python


from benchflow.task.benchmark import HuggingfaceTransformers,FlagOpenFlagPerf
from benchflow.modelzoo.model_meta import ModelInfoParser

# You can use the ModelInfo class and model_info_list as needed in your benchflow.py file

import pandas as pd


def run_benchflow():
    import argparse

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
        "--task",
        choices=["POC", "benchmark", "automatic_search"],
        nargs="?",
        help="The machine learning task to benchmark (choose from 'POC', 'benchmark', or 'automatic_search').",
    )
    parser.add_argument(
        "--list",
        dest="list",
        action="store_true",
        help="If provided, benchmark multiple machine learning models.",
    )
    args = parser.parse_args()


    if args.task == "POC":
        print("Benchmarking POC task...")
        # Your POC benchmarking code here
    elif args.task == "benchmark":
        print("Benchmarking benchmark task...")
        # Your benchmarking code here
    elif args.task == "automatic_search":
        print("Benchmarking automatic_search task...")
        # Your automatic_search benchmarking code here

    if args.list:
        print("\033[1m\033[33mBenchmarking multiple models:\033[0m")
        parser = ModelInfoParser()
        model_info_list = parser.parse_csv_file()
        parser.print_model_info_list_with_pandas(model_info_list)

if __name__ == "__main__":
    run_benchflow()
