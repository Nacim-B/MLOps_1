import gzip
from io import BytesIO, StringIO
import pandas as pd
import boto3
import pickle

class S3Handler:
    def __init__(self, bucket: str, config: dict):
        self.bucket = bucket
        self.s3 = boto3.client("s3")
        self.config = config


    def load_csv_from_s3(self, key: str) -> pd.DataFrame:
        """
        Reads a CSV file from S3 (supports gzip if needed).

        Args:
            key (str): Full key (path) to the CSV file in S3

        Returns:
            pd.DataFrame: The loaded DataFrame
        """

        response = self.s3.get_object(Key=key, Bucket=self.bucket)
        raw = response["Body"].read()

        if raw[:2] == b"\x1f\x8b":
            print("🌀 GZIP compression detected")
            with gzip.open(BytesIO(raw), mode="rt") as f:
                return pd.read_csv(f)
        else:
            print("📄 Plain CSV detected")
            if self.config['csv_separator'] and 'processed' not in key:
                return pd.read_csv(StringIO(raw.decode("utf-8")), sep=self.config['csv_separator'])
            else:
                return pd.read_csv(StringIO(raw.decode("utf-8")))

    def load_model_from_s3(self, key: str):
        """
        Loads a pickled model from S3.

        Args:
            key (str): Key/path to the pickled model file in S3.

        Returns:
            The deserialized model object.
        """

        response = self.s3.get_object(Bucket=self.bucket, Key=key)
        model = pickle.load(response["Body"])
        print(f"✅ Loaded model from s3://{self.bucket}/{key}")
        return model

    def save_csv_to_s3(self, df: pd.DataFrame, key: str, index: bool = True):
        """
        Saves a pandas DataFrame as CSV to S3.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            key (str): Path/key in S3 bucket.
            index (bool): Whether to include the index in the CSV. Default is True.
        """
        buffer = StringIO()
        df.to_csv(buffer, index=index)
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=buffer.getvalue())


    def save_model_to_s3(self, model, key: str):
        """
        Save a model object to S3 using pickle.

        Args:
            model: The model object to serialize.
            key (str): Destination path in S3.
        """
        buffer = BytesIO()
        pickle.dump(model, buffer)
        buffer.seek(0)

        self.s3.put_object(Bucket=self.bucket, Key=key, Body=buffer.getvalue())
        print(f"✅ Model saved to s3://{self.bucket}/{key}")

    def exists_in_s3(self, key: str) -> bool:
        """
        Check if a given key exists in the S3 bucket.

        Args:
            key (str): The object key to check (e.g., 'models/my_model.pkl').

        Returns:
            bool: True if the object exists, False otherwise.
        """
        try:
            self.s3.head_object(Bucket=self.bucket, Key=key)
            return True
        except self.s3.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                raise