import os
from dotenv import load_dotenv
from mlops_project.config.config_loader import load_config
from mlops_project.utils.data_processing import DataProcessor

def data_processing():
    load_dotenv()
    config = load_config("../config/dev.yaml")

    csv_raw_key = f"datasets/{os.getenv("CSV_FILENAME")}_raw.csv"
    csv_processed_key = f"datasets/{os.getenv("CSV_FILENAME")}_processed.csv"

    data_processor = DataProcessor(
        os.getenv("S3_BUCKET_NAME"),
        csv_raw_key=csv_raw_key,
        csv_processed_key=csv_processed_key,
        config=config
    )

    data_processor.run()

if __name__ == "__main__":
    data_processing()
