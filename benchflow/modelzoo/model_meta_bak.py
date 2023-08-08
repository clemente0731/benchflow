from dataclasses import dataclass
import pandas as pd
import pkg_resources
import os


class ModelInfo:
    @dataclass
    class Info:
        model_id: int
        model_name: str
        num_devices: str
        model_classification: str
        github_url: str
        commit: str
        execution_path: str
        dataset_download_source: str
        dataset_relative_directory: str
        default_batch_size: int
        execution_command: str
        environment_variables: str
        source_code_modified: int

    def __init__(self, info):
        self.info = info


class ModelInfoParser:
    def __init__(self, file_path=None):
        """
        ModelInfoParser类的构造函数。

        Parameters:
            file_path (str, optional): CSV文件的路径。默认为None，表示使用默认的文件路径。
        """
        if file_path is None:
            file_path = self.get_csv_file_path()
        self.file_path = file_path

    def get_csv_file_path(self):
        """
        获取CSV文件的路径。

        Returns:
            str: CSV文件的绝对或相对路径。
        """
        custom_file_path = os.environ.get("BENCHFLOW_CSV_FILE_PATH")
        if custom_file_path:
            return custom_file_path
        return pkg_resources.resource_filename(
            "benchflow", "configs/registered_models.csv"
        )

    def read_csv_file(self, file_path=None):
        """
        从CSV文件中读取数据，并将其转换为ModelInfo对象列表。

        Parameters:
            file_path (str, optional): CSV文件的路径。默认为None，表示使用初始化时指定的文件路径。

        Returns:
            list: 包含ModelInfo对象的列表。
        """
        if file_path is None:
            file_path = self.file_path

        df = pd.read_csv(file_path)

        model_info_list = []
        for _, row in df.iterrows():
            info = ModelInfo.Info(
                model_id=row["model_id"],
                model_name=row["model_name"],
                num_devices=row["num_devices"],
                model_classification=row["model_classification"],
                github_url=row["github_url"],
                commit=row["commit"],
                execution_path=row["execution_path"],
                dataset_download_source=row["dataset_download_source"],
                dataset_relative_directory=row["dataset_relative_directory"],
                default_batch_size=row["default_batch_size"],
                execution_command=row["execution_command"],
                environment_variables=row["environment_variables"],
                source_code_modified=row["source_code_modified"],
            )
            model_info = ModelInfo(info)
            model_info_list.append(model_info)

        return model_info_list

    def parse_csv_file(self, file_path=None):
        """
        解析CSV文件，将其中的数据转换为ModelInfo对象列表。

        Parameters:
            file_path (str, optional): CSV文件的路径。默认为None，表示使用初始化时指定的文件路径。

        Returns:
            list: 包含ModelInfo对象的列表。
        """
        if file_path is not None:
            self.file_path = file_path

        return self.read_csv_file()

    def print_model_info_list(self, model_info_list=None):
        """
        打印ModelInfo对象列表的信息。

        Parameters:
            model_info_list (list, optional): 包含ModelInfo对象的列表。默认为None，表示使用parse_csv_file方法返回的列表。
        """
        if model_info_list is None:
            model_info_list = self.parse_csv_file()

        print(
            "{:<5} {:<25} {:<10} {:<20} {:<60} {:<10} {:<40} {:<40} {:<40} {:<10} {:<100} {:<40} {:<10}".format(
                "ID",
                "Name",
                "Num Devices",
                "Classification",
                "GitHub URL",
                "Commit",
                "Execution Path",
                "Download Source",
                "Relative Directory",
                "Batch Size",
                "Execution Command",
                "Environment Variables",
                "Source Code Modified",
            )
        )

        for model_info in model_info_list:
            info = model_info.info
            print(
                "{:<5} {:<25} {:<10} {:<20} {:<60} {:<10} {:<40} {:<40} {:<40} {:<10} {:<100} {:<40} {:<10}".format(
                    info.model_id,
                    info.model_name,
                    info.num_devices,
                    info.model_classification,
                    info.github_url,
                    info.commit,
                    info.execution_path,
                    info.dataset_download_source,
                    info.dataset_relative_directory,
                    info.default_batch_size,
                    info.execution_command,
                    info.environment_variables,
                    info.source_code_modified,
                )
            )

    def print_model_info_list_with_pandas(self, model_info_list=None):
        """
        打印ModelInfo对象列表的信息。

        Parameters:
            model_info_list (list, optional): 包含ModelInfo对象的列表。默认为None，表示使用parse_csv_file方法返回的列表。
        """
        if model_info_list is None:
            model_info_list = self.parse_csv_file()

        data = []
        for model_info in model_info_list:
            info = model_info.info
            data.append(
                [
                    info.model_id,
                    info.model_name,
                    info.num_devices,
                    info.model_classification,
                    info.github_url,
                    info.commit,
                    info.execution_path,
                    info.dataset_download_source,
                    info.dataset_relative_directory,
                    info.default_batch_size,
                    info.execution_command,
                    info.environment_variables,
                    info.source_code_modified,
                ]
            )

        columns = [
            "ID",
            "Name",
            "Num Devices",
            "Classification",
            "GitHub URL",
            "Commit",
            "Execution Path",
            "Download Source",
            "Relative Directory",
            "Batch Size",
            "Execution Command",
            "Environment Variables",
            "Source Code Modified",
        ]

        # Get the maximum length for each column
        max_lengths = [len(col) for col in columns]
        max_len_limit = 30  # Maximum allowed length for each value in the table

        # Truncate long strings to max_len_limit
        for row in data:
            for i, value in enumerate(row):
                str_value = str(value)
                if len(str_value) > max_len_limit:
                    row[i] = str_value[: max_len_limit - 3] + "..."
                max_lengths[i] = max(max_lengths[i], len(str(row[i])))

        # Format the table header
        header = " | ".join(f"{col:<{max_lengths[i]}}" for i, col in enumerate(columns))
        separator = "-" * len(header)

        # Format the table data rows
        table_rows = [header, separator]
        for row in data:
            table_row = " | ".join(
                f"{str(value):<{max_lengths[i]}}" for i, value in enumerate(row)
            )
            table_rows.append(table_row)

        # Print the table
        for row in table_rows:
            print(row)
