import os
import pandas as pd
from mlops_project.utils.s3_handler import S3Handler
from mlops_project.config.mysql_handler import MySQLHandler


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
            self.mysql_handler = MySQLHandler()


    def run(self) -> pd.DataFrame:
        """
        Load the dataset depending on the source type.
        """

        if self.data_source == 'csv_url':
            self.s3_handler.upload_csv_from_url_to_s3(
                os.getenv("CSV_URL"),
                os.getenv("CSV_FILENAME")
            )
            return self.s3_handler.load_csv_from_s3(f"datasets/{os.getenv("CSV_FILENAME")}_raw.csv")

        elif self.data_source  == 'csv_s3':
            return self.s3_handler.load_csv_from_s3(f"datasets/{os.getenv("CSV_FILENAME")}_processed.csv")

        elif self.data_source  == 'mysql':
            return self.mysql_handler.execute_query('select_all')
        else:
            raise ValueError(f"Unknown data source type: {self.data_source}")


