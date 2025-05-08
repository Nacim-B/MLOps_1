import os
from io import StringIO
import pandas as pd
import requests
from mlops_project.utils.mysql_handler import MySQLHandler
from mlops_project.utils.s3_handler import S3Handler


class DataLoader:
    def __init__(self, config: dict):
        """
        Initialize the DataLoader with the project configuration.
        """
        self.config = config
        self.data_source = self.config['data_source']
        self.s3_handler = S3Handler(
                bucket=os.getenv("S3_BUCKET_NAME"),
                config=self.config
            )
        if self.data_source == "mysql":
            self.mysql_handler = MySQLHandler(self.config)


    def run(self) -> pd.DataFrame:
        """
        Load the dataset depending on the source type.
        """

        if self.data_source == 'csv_url':
            return self.load_csv_from_url(os.getenv("CSV_URL"))

        if self.data_source == 'csv_s3':
            return self.s3_handler.load_csv_from_s3(self.config['s3_csv_key'])

        elif self.data_source  == 'mysql':
            df = self.mysql_handler.load_data_from_db("select_all")
            print(df.shape)
            return df
        else:
            raise ValueError(f"Unknown data source type: {self.data_source}")


    def load_csv_from_url(self, url: str, columns: list = None) -> pd.DataFrame:
        """
        Downloads a CSV from a public URL and returns it as a pandas DataFrame.

        Args:
            url (str): The public URL pointing to the CSV file.
            columns (list, optional): List of column names to assign to the DataFrame.

        Returns:
            pd.DataFrame: The loaded DataFrame.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            print(f"✅ CSV downloaded from {url}")
            csv_content = response.text
            df = pd.read_csv(StringIO(csv_content), names=columns, sep=self.config['csv_separator'])
            return df
        except requests.RequestException as e:
            print(f"❌ Failed to download CSV: {e}")
            raise


