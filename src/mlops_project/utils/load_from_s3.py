import gzip
from io import BytesIO, StringIO
import pandas as pd
import boto3
import pickle

class S3Loader:
    def __init__(self, bucket: str):
        self.bucket = bucket
        self.s3 = boto3.client("s3")

    def load_csv_from_s3(self, key: str) -> pd.DataFrame:
        """
        Reads a CSV file from S3 (supports gzip if needed).

        Args:
            key (str): Full key (path) to the CSV file in S3

        Returns:
            pd.DataFrame: The loaded DataFrame
        """
        response = self.s3.get_object(Bucket=self.bucket, Key=key)
        raw = response["Body"].read()

        if raw[:2] == b"\x1f\x8b":
            print("🌀 GZIP compression detected")
            with gzip.open(BytesIO(raw), mode="rt") as f:
                return pd.read_csv(f)
        else:
            print("📄 Plain CSV detected")
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