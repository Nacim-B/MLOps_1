import gzip
from io import BytesIO, StringIO
import pandas as pd
import boto3


def read_csv_from_s3(bucket: str, key: str) -> pd.DataFrame:
    """
    Reads a CSV file from S3 (supports gzip if needed).

    Args:
        bucket (str): Name of the S3 bucket
        key (str): Full key (path) to the CSV file in S3

    Returns:
        pd.DataFrame: The loaded DataFrame
    """
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    raw = response["Body"].read()

    if raw[:2] == b"\x1f\x8b":
        print("🌀 GZIP compression detected")
        with gzip.open(BytesIO(raw), mode="rt") as f:
            return pd.read_csv(f)
    else:
        print("📄 Plain CSV detected")
        return pd.read_csv(StringIO(raw.decode("utf-8")))
