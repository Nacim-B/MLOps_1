import os
from dotenv import load_dotenv
from mlops_project.data.fetch_data import DataFetcher

def main():
    load_dotenv()

    bucket = os.getenv("S3_BUCKET_NAME")
    url = os.getenv("CSV_URL")
    filename = os.getenv("CSV_FILENAME", "raw_data.csv")

    if not bucket or not url:
        raise ValueError("Missing S3_BUCKET_NAME or CSV_URL.")

    fetcher = DataFetcher(bucket_name=bucket)
    fetcher.upload_csv_from_url(url=url, filename=filename)

if __name__ == "__main__":
    main()
