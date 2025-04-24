import os
from dotenv import load_dotenv
from mlops_project.config.config_loader import load_config
from mlops_project.utils.data_processing import DataProcessor

def data_processing():
    load_dotenv()
    config = load_config("../config/dev.yaml")

    bucket = os.getenv("S3_BUCKET_NAME")
    filename = os.getenv("CSV_FILENAME")

    data_processor = DataProcessor(
        bucket,
        f"datasets/{filename}_raw.csv",
        f"datasets/{filename}_processed.csv",
        config=config
    )

    data_processor.run()

if __name__ == "__main__":
    data_processing()
