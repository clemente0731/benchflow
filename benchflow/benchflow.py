#!/usr/bin/env python

from abc import ABC, abstractmethod


import pandas as pd


def parse_csv_file(file_path):
    df = pd.read_csv(file_path)

    model_ids = df["model_id"]
    model_names = df["model_name"]
    num_devices = df["num_devices"]
    model_classification = df["model_classification"]
    github_urls = df["github_url"]
    commits = df["commit"]
    execution_paths = df["execution_path"]
    dataset_download_sources = df["dataset_download_source"]
    dataset_relative_directories = df["dataset_relative_directory"]
    execution_commands = df["execution_command"]
    environment_variables = df["environment_variables"]
    source_code_modified = df["source_code_modified"]

    # Process the data or use it as required

    # Example: Print all model names
    for model_name in model_names:
        print(model_name)


# Replace 'file_path' with the actual path to your CSV file
csv_file_path = "./configs/registered_models.csv"
parse_csv_file(csv_file_path)


class OpenModelZooBenchmark(ABC):
    def benchmark(self):
        """
        Execute the benchmark process.
        """
        self.load_model()
        self.prepare_data()
        self.run_inference()
        self.collect_results()

    @abstractmethod
    def load_model(self):
        """
        Load the model for benchmarking.
        """
        pass

    @abstractmethod
    def prepare_data(self):
        """
        Prepare the data for the benchmarking process.
        """
        pass

    @abstractmethod
    def run_inference(self):
        """
        Run the inference using the loaded model.
        """
        pass

    def collect_results(self):
        """
        Collect and analyze performance results.
        """
        print("Collecting and analyzing performance results...")


class HuggingfaceTransformers(OpenModelZooBenchmark):
    def load_model(self):
        """
        Load Model A from Huggingface Transformers.
        """
        print("Loading Model A...")

    def prepare_data(self):
        """
        Prepare data for Model A from Huggingface Transformers.
        """
        print("Preparing data for Model A...")

    def run_inference(self):
        """
        Run inference using Model A from Huggingface Transformers.
        """
        print("Running inference using Model A...")


class FlagOpenFlagPerf(OpenModelZooBenchmark):
    def load_model(self):
        """
        Load Model B from FlagOpenFlagPerf.
        """
        print("Loading Model B...")

    def prepare_data(self):
        """
        Prepare data for Model B from FlagOpenFlagPerf.
        """
        print("Preparing data for Model B...")

    def run_inference(self):
        """
        Run inference using Model B from FlagOpenFlagPerf.
        """
        print("Running inference using Model B...")


def run_benchflow():
    import argparse

    parser = argparse.ArgumentParser(
        description="Benchmark machine learning models using the OpenModelZooBenchmark template class."
    )
    parser.add_argument(
        "model",
        choices=["huggingface", "flagopenflagperf"],
        help="The machine learning model to benchmark (choose from 'huggingface' or 'flagopenflagperf').",
    )
    args = parser.parse_args()

    if args.model == "huggingface":
        print("Benchmarking Model A from Huggingface Transformers...")
        model_a = HuggingfaceTransformers()
        model_a.benchmark()
    elif args.model == "flagopenflagperf":
        print("Benchmarking Model B from FlagOpenFlagPerf...")
        model_b = FlagOpenFlagPerf()
        model_b.benchmark()


if __name__ == "__main__":
    run_benchflow()
