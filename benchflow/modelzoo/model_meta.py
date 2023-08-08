from dataclasses import dataclass, field
import pandas as pd
import pkg_resources
import os
from pprint import pprint

MAX_COL_WIDTH_LIMIT = 120


class ModelInfoLoader:
    def __init__(self, csv_file_path=None):
        self.csv_file_path = csv_file_path or self.get_csv_file_path()

    def get_csv_file_path(self):
        custom_file_path = os.environ.get("BENCHFLOW_CSV_FILE_PATH")
        if custom_file_path:
            return custom_file_path
        return pkg_resources.resource_filename(
            "benchflow", "configs/registered_models.csv"
        )

    def load_model_info(self, csv_file_path=None):
        csv_file_path = csv_file_path or self.csv_file_path
        df = pd.read_csv(csv_file_path)
        model_info_list = []

        for _, row in df.iterrows():
            pprint(row.to_dict())
            model_info_list.append(row.to_dict())

        return model_info_list

    def print_model_info_list(self, model_info_list=None):
        model_info_list = model_info_list or self.load_model_info()
        columns = model_info_list[0].keys()

        # Calculate the maximum width for each column based on the average element length
        max_col_widths = {}

        for col in columns:
            # Calculate the total length of all elements in the current column
            total_length = sum(len(str(info[col])) for info in model_info_list)
            avg_length = total_length / len(model_info_list)

            # If the column is "model_id", adjust the average length to prevent the serial number from being truncated
            if col == "model_id":
                avg_length = (
                    total_length / len(model_info_list) + 5
                )  # Add a correction to prevent truncation of the serial number
            # Set the maximum column width as the minimum of the average length and the maximum width limit
            max_col_widths[col] = min(int(avg_length), MAX_COL_WIDTH_LIMIT)

        color_map = {column: f"\033[3{idx % 6}m" for idx, column in enumerate(columns)}

        header = " | ".join(f"{col}" for col in columns)
        separator = "-" * len(header)

        colored_header = " | ".join(f"{color_map[col]}{col}\033[0m" for col in columns)

        print(separator)
        print(colored_header)
        print(separator)

        for info in model_info_list:
            # Initialize an empty list to store colored values
            colored_values = []
            # Iterate over columns and build colored values
            for col in columns:
                colored_value = f"{color_map[col]}{str(info[col])[:max_col_widths[col]]:<{max_col_widths[col]}}\033[0m"
                colored_values.append(colored_value)

            print(" | ".join(colored_values))
