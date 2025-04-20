import boto3
import requests


class DataFetcher:
    def __init__(self, bucket_name: str, s3_prefix: str = "datasets/"):
        self.bucket_name = bucket_name
        self.s3_prefix = s3_prefix
        self.s3 = boto3.client("s3")

    def upload_csv_from_url(self, url: str, filename: str):
        """
        Fetches a CSV file from a public URL and uploads it to the S3 bucket
        under the datasets/ folder.
        """
        s3_key = f"{self.s3_prefix}{filename}"

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            self.s3.upload_fileobj(response.raw, self.bucket_name, s3_key)
            print(f"✅ CSV uploaded to s3://{self.bucket_name}/{s3_key}")

        except requests.RequestException as e:
            print(f"❌ Failed to download CSV: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    def upload_csv_from_rds(self, query: str, filename: str, connection_params: dict):
        """
        Placeholder for future functionality to extract data from RDS,
        convert to CSV, and upload to S3.
        """
        raise NotImplementedError("This method will handle RDS extraction in the future.")
