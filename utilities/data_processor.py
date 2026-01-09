import os
import pandas as pd
from io import StringIO


class DataProcessor:
    """Loads data from a CSV file and provides methods to summarize it."""

    def __init__(self, file_path: str):
        """
        Initializes the DataProcessor by loading a CSV file into a pandas DataFrame.

        Args:
            file_path: The path to the CSV file.

        Raises:
            FileNotFoundError: If the file does not exist at the given path.
            pd.errors.EmptyDataError: If the CSV file is empty.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No file found at the specified path: {file_path}")
        self.df = pd.read_csv(file_path)

    def generate_prompt_summary(self, num_rows: int = 5) -> str:
        """
        Generates a text-based summary of the dataframe for use in an LLM prompt.

        The summary includes the columns, their data types, and the first few
        rows of data.

        Args:
            num_rows: The number of rows to include in the data sample.

        Returns:
            A formatted string containing the dataframe summary.
        """
        # Use StringIO to build the string summary efficiently
        summary_io = StringIO()

        summary_io.write("Here is a summary of the dataframe:\n\n")
        summary_io.write("Columns and their data types:\n")
        for col, dtype in self.df.dtypes.items():
            summary_io.write(f"- {col}: {dtype}\n")

        summary_io.write(f"\nFirst {num_rows} rows of data:\n")
        summary_io.write(self.df.head(num_rows).to_string())

        return summary_io.getvalue()