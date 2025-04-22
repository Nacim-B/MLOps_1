import os
from dotenv import load_dotenv
from mlops_project.config.config_loader import load_config
from mlops_project.utils.modelisation import ModelTrainer

def main():
    load_dotenv()
    config = load_config("../config/dev.yaml")

    bucket = os.getenv("S3_BUCKET_NAME")
    filename = os.getenv("CSV_FILENAME")
    csv_processed_key = f"datasets/{filename}_processed.csv"
    model_key = f"models/logisticregression_final.pkl"

    trainer = ModelTrainer(
        bucket=bucket,
        csv_processed_key=csv_processed_key,
        model_key=model_key,
        config=config
    )
    trainer.run()

if __name__ == "__main__":
    main()