import os
from dotenv import load_dotenv
from mlops_project.utils.s3_handler import S3Handler

def download_raw_csv():
    load_dotenv()

    bucket = os.getenv("S3_BUCKET_NAME")
    url = os.getenv("CSV_URL")
    filename = os.getenv("CSV_FILENAME", "raw_data.csv")

    if not bucket or not url:
        raise ValueError("Missing S3_BUCKET_NAME or CSV_URL.")

    fetcher = S3Handler(bucket)
    fetcher.upload_csv_from_url_to_s3(url=url, filename=filename)

if __name__ == "__main__":
    download_raw_csv()
