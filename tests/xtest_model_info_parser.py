import unittest
import sys
from io import StringIO
from benchflow.modelzoo.model_meta import ModelInfoLoader
from contextlib import contextmanager

class TestModelInfoLoader(unittest.TestCase):
    @contextmanager
    def capture_output(self):
        """
        Context manager to capture stdout output for testing.
        """
        old_out = sys.stdout
        new_out = StringIO()
        sys.stdout = new_out
        try:
            yield new_out
        finally:
            sys.stdout = old_out

    def test_print_model_info_list(self):
        # Define a mock data to use for testing
        mock_data = [
            {"model_id": "1", "name": "Model A", "type": "Type A"},
            {"model_id": "2", "name": "Model B", "type": "Type B"}
        ]

        # Create an instance of ModelInfoLoader
        loader = ModelInfoLoader()

        # Mock the load_model_info method to return mock_data
        loader.load_model_info = lambda csv_file_path=None: mock_data
        expected_output = (
            "----------------------------------------------\n"
            "\033[31mmodel_id\033[0m   | \033[32mname\033[0m               | \033[33mtype\033[0m               \n"
            "----------------------------------------------\n"
            "\033[31m1\033[0m        | \033[32mModel A\033[0m           | \033[33mType A\033[0m           \n"
            "\033[31m2\033[0m        | \033[32mModel B\033[0m           | \033[33mType B\033[0m           \n"
        )

        # Capture the stdout output during the test
        with self.capture_output() as output:
            loader.print_model_info_list()

        # Check if the expected content is present in the printed output
        self.assertIn("model_id", output.getvalue())
        self.assertIn("Model A", output.getvalue())
        self.assertIn("Type B", output.getvalue())


if __name__ == "__main__":
    unittest.main()
