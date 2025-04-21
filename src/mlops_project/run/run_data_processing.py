import os
from dotenv import load_dotenv
from mlops_project.utils.data_processing import DataProcessor

def data_processing():
    load_dotenv()

    bucket = os.getenv("S3_BUCKET_NAME")
    filename = os.getenv("CSV_FILENAME", "raw_data.csv")

    data_processor = DataProcessor(
        bucket,
        f"datasets/{filename}_raw.csv",
        f"datasets/{filename}_processed.csv",
        "Survived",
        "PassengerId"
    )

    data_processor.run()

if __name__ == "__main__":
    data_processing()
